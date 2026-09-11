"""
Add timed male voiceover to the demo screen recording.

Always uses the ORIGINAL screen recording as the video source.
The output file is never used as input.

Edit SubmissionDocument/narration_prompt.txt:
    start_sec|Your narration line here

Author: Vivek Kumar
"""

import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

import edge_tts
import imageio_ffmpeg
import numpy as np
from moviepy import AudioFileClip, CompositeAudioClip, VideoFileClip
from moviepy.audio.AudioClip import AudioArrayClip

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = Path(r"D:\_GenAIProject\BKp\Enterprise_Knowledge_Assistant_temp")
CONFIG_PATH = WORK_DIR / "narration_config.json"
SEGMENTS_DIR = WORK_DIR / "narration_segments"
DEFAULT_CAPTURES_DIR = Path.home() / "Videos" / "Captures"


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        return json.load(config_file)


def resolve_source_video(config: dict, output_video: Path) -> Path:
    """Return the original screen recording. Never use the narrated output."""
    configured = config.get("source_video") or config.get("input_video")
    if not configured:
        raise ValueError("narration_config.json must set source_video to the original recording.")

    source = Path(configured).expanduser().resolve()
    output = output_video.resolve()

    if source == output:
        raise ValueError("source_video must be the original recording, not the narrated output.")

    if source.exists():
        return source

    # Fallback: newest Oeeggis capture in the default folder.
    if DEFAULT_CAPTURES_DIR.exists():
        candidates = sorted(
            DEFAULT_CAPTURES_DIR.glob("*Oeeggis*Enterprise Knowledge Assistant*.mp4"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        for candidate in candidates:
            if candidate.resolve() != output and "narration" not in candidate.name.lower():
                print(f"WARNING: Configured source not found. Using capture:\n  {candidate}")
                return candidate.resolve()

    raise FileNotFoundError(f"Original screen recording not found:\n{source}")


def load_segments_from_prompt(prompt_path: Path) -> list[dict]:
    segments = []
    pattern = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*\|\s*(.+?)\s*$")

    for line in prompt_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = pattern.match(stripped)
        if not match:
            continue
        segments.append(
            {
                "start_sec": float(match.group(1)),
                "text": match.group(2).strip(),
            }
        )

    if not segments:
        raise ValueError(f"No narration lines found in {prompt_path}")

    return segments


async def generate_segment_audio(text: str, output_path: Path, voice: str) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))


async def generate_all_segments(segments: list[dict], voice: str, output_dir: Path) -> list[dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    prepared = []

    for index, segment in enumerate(segments):
        audio_path = output_dir / f"segment_{index:02d}.mp3"
        await generate_segment_audio(segment["text"], audio_path, voice)
        prepared.append(
            {
                "start_sec": float(segment["start_sec"]),
                "text": segment["text"],
                "audio_path": audio_path,
            }
        )
        print(f"  [{index + 1}/{len(segments)}] {segment['start_sec']}s -> {segment['text'][:60]}...")

    return prepared


def build_timed_audio_track(segments: list[dict], video_duration: float) -> AudioFileClip:
    audio_clips = [
        AudioFileClip(str(segment["audio_path"])).with_start(segment["start_sec"])
        for segment in segments
    ]

    composite = CompositeAudioClip(audio_clips)

    if composite.duration < video_duration:
        silence_duration = video_duration - composite.duration
        fps = 44100
        samples = max(1, int(silence_duration * fps))
        silence = AudioArrayClip(np.zeros((samples, 2)), fps=fps).with_start(composite.duration)
        composite = CompositeAudioClip([composite, silence])

    return composite.with_duration(video_duration)


def save_combined_mp3(audio: AudioFileClip, output_path: Path) -> None:
    audio.write_audiofile(str(output_path), logger=None)


def mux_voice_onto_source_video(source_video: Path, narration_audio: Path, output_video: Path) -> None:
    """Copy original video stream and attach narration audio (no video re-encode)."""
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    output_video.parent.mkdir(parents=True, exist_ok=True)

    command = [
        ffmpeg,
        "-y",
        "-i",
        str(source_video),
        "-i",
        str(narration_audio),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(output_video),
    ]

    print("Muxing narration onto original video (video stream copy)...")
    subprocess.run(command, check=True)


def validate_output(source_video: Path, output_video: Path) -> None:
    source_mb = source_video.stat().st_size / (1024 * 1024)
    output_mb = output_video.stat().st_size / (1024 * 1024)

    if output_mb < source_mb * 0.5:
        raise RuntimeError(
            "Output video looks too small. Expected near-original quality.\n"
            f"  Source: {source_mb:.1f} MB\n"
            f"  Output: {output_mb:.1f} MB"
        )


def main() -> int:
    config = load_config()
    output_video = (PROJECT_ROOT / "SubmissionDocument" / config["output_video"]).resolve()
    output_audio = PROJECT_ROOT / "SubmissionDocument" / config.get("output_audio", "demo_narration_male.mp3")
    prompt_file = PROJECT_ROOT / "SubmissionDocument" / config.get("prompt_file", "narration_prompt.txt")
    voice = config.get("voice", "en-US-GuyNeural")

    source_video = resolve_source_video(config, output_video)

    if not prompt_file.exists():
        print(f"ERROR: Narration prompt not found:\n{prompt_file}")
        return 1

    segments = load_segments_from_prompt(prompt_file)

    print(f"Source video (original recording): {source_video}")
    print(f"Output video: {output_video}")
    print(f"Voice: {voice}")
    print(f"Prompt file: {prompt_file}")
    print(f"Segments: {len(segments)}")
    print("Generating narration audio...")
    prepared_segments = asyncio.run(generate_all_segments(segments, voice, SEGMENTS_DIR))

    print("Reading source video duration...")
    video = VideoFileClip(str(source_video))
    video_duration = video.duration
    print(f"Source duration: {video_duration:.1f}s | size: {video.size} | fps: {video.fps:.2f}")
    video.close()

    print("Building timed audio track...")
    final_audio = build_timed_audio_track(prepared_segments, video_duration)
    print(f"Audio duration: {final_audio.duration:.1f}s")

    print(f"Saving audio only: {output_audio}")
    save_combined_mp3(final_audio, output_audio)
    final_audio.close()

    mux_voice_onto_source_video(source_video, output_audio, output_video)
    validate_output(source_video, output_video)

    output_mb = output_video.stat().st_size / (1024 * 1024)
    print("Done.")
    print(f"Source: {source_video}")
    print(f"Audio: {output_audio}")
    print(f"Video: {output_video} ({output_mb:.1f} MB)")
    print("Edit narration_prompt.txt start_sec values if timing is off, then run again.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
