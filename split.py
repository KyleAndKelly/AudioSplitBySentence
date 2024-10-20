import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

def process_audio(input_audio_dir, output_audio_dir, min_silence_len=2000, silence_thresh=-40, keep_silence=200):
    """
    分割音频文件为句子段落，并生成短音频文件
    """
    if not os.path.exists(output_audio_dir):
        os.makedirs(output_audio_dir)

    # 读取 input_audio_dir 下的所有音频文件
    audio_files = [f for f in os.listdir(input_audio_dir) if f.endswith(('.wav', '.mp3', '.m4a'))]

    # 遍历每个音频文件
    for audio_file in audio_files:
        audio_path = os.path.join(input_audio_dir, audio_file)
        audio = AudioSegment.from_file(audio_path)
        audio_name = os.path.splitext(audio_file)[0]

        # 分割音频为每个句子
        chunks = split_on_silence(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,
            keep_silence=keep_silence
        )

        # 处理每个音频块，生成音频
        for idx, chunk in enumerate(chunks):
            # 导出短音频
            chunk_file_name = f"{audio_name}_{idx+1}.wav"
            chunk_file_path = os.path.join(output_audio_dir, chunk_file_name)
            chunk.export(chunk_file_path, format="wav")

            print(f"处理完成: {chunk_file_name}")

if __name__ == "__main__":
    # 示例：设置输入输出目录，处理音频文件
    input_audio_dir = "./input"  # 输入音频文件夹路径
    output_audio_dir = "./output"  # 输出音频文件夹路径

    process_audio(input_audio_dir, output_audio_dir)
