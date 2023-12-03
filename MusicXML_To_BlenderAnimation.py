#This version is a development version released on GitHub and may contain bugs.
#The official version to be released on Blender Market is expected to include a piano model.
#Made by HoloMoto (email:seirios48@yahoo.co.jp  twitter;@HoloMotoRanger ) I Love MixedReality And HoloLens.

import bpy
from music21 import *

def get_tempo_from_musicxml(score):
    metronome_marks = score.flat.getElementsByClass('MetronomeMark')
    if metronome_marks:
        return metronome_marks[0].getQuarterBPM()
    else:
        return None

def get_animation_length_from_musicxml(score):
    tempo = get_tempo_from_musicxml(score)
    
    if tempo:
        # 小節の長さを取得
        measures = len(score.parts[0].getElementsByClass(stream.Measure))
        
        # アニメーションの長さを計算
        quarter_note_duration = 60 / tempo  # テンポによる一拍の時間（秒）
        animation_length = quarter_note_duration * 4 * measures  # 四分音符の数 × 小節の数
        return animation_length, quarter_note_duration
    else:
        return None, None

def pitch_to_note_name(pitch):
    # MIDIノート番号を音名に変換
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = pitch // 12 - 1
    note_name = note_names[pitch % 12]
    return f"{note_name}{octave}"

def set_keyframes_from_musicxml(file_path, object_prefix, target_fps=24):
    # MusicXMLファイルを読み込む
    score = converter.parse(file_path)

    # アニメーションの長さと四分音符の長さを取得
    animation_length, quarter_note_duration = get_animation_length_from_musicxml(score)

    if animation_length is None:
        print("Failed to get the length of the animation.")
        return

    # キーフレームを打ち込むための基本的なパラメータ
    frame_start = 1  # アニメーションの開始フレーム
    frame_end = int(target_fps * animation_length)  # アニメーションの終了フレーム

    # ターゲットのFPSを設定
    frame_rate = target_fps  # ターゲットのFPSを設定

    for part in score.parts:
        for element in part.flat:
            if isinstance(element, note.Note):
                # オブジェクト名を作成
                object_name = f"{object_prefix}{pitch_to_note_name(element.pitch.midi)}"

                # オブジェクトが存在しない場合はスキップ
                if not bpy.data.objects.get(object_name):
                    # _ がない場合も考慮
                    object_name = f"{object_prefix}_{pitch_to_note_name(element.pitch.midi)}"
                    if not bpy.data.objects.get(object_name):
                        print(f"Object '{object_name}' is not found。")
                        continue

                # オブジェクトを取得
                piano_object = bpy.data.objects[object_name]

                # キーフレームを設定
                frame = int(element.offset / quarter_note_duration * target_fps) + frame_start
                piano_object.location.z = 0.0
                piano_object.keyframe_insert(data_path="location", index=2, frame=frame)

                # 沈むアニメーション
                sink_frame = int((element.offset + element.duration.quarterLength / 2) / quarter_note_duration * target_fps) + frame_start
                piano_object.location.z = -1.0
                piano_object.keyframe_insert(data_path="location", index=2, frame=sink_frame)

                # 戻るアニメーション
                rise_frame = int((element.offset + element.duration.quarterLength) / quarter_note_duration * target_fps) + frame_start
                piano_object.location.z = 0.0
                piano_object.keyframe_insert(data_path="location", index=2, frame=rise_frame)

            elif isinstance(element, chord.Chord):
                for pitch in element.pitches:
                    # Create Object
                    object_name = f"{object_prefix}{pitch_to_note_name(pitch.midi)}"

                    # オブジェクトが存在しない場合はスキップ
                    if not bpy.data.objects.get(object_name):
                        # _ がない場合も考慮
                        object_name = f"{object_prefix}_{pitch_to_note_name(pitch.midi)}"
                        if not bpy.data.objects.get(object_name):
                            print(f"Object '{object_name}'is not found")
                            continue

                    # オブジェクトを取得
                    piano_object = bpy.data.objects[object_name]

                    # キーフレームを設定
                    frame = int(element.offset / quarter_note_duration * target_fps) + frame_start
                    piano_object.location.z = 0.0
                    piano_object.keyframe_insert(data_path="location", index=2, frame=frame)

                    # 沈むアニメーション
                    sink_frame = int((element.offset + element.duration.quarterLength / 2) / quarter_note_duration * target_fps) + frame_start
                    piano_object.location.z = -1.0
                    piano_object.keyframe_insert(data_path="location", index=2, frame=sink_frame)

                    # 戻るアニメーション
                    rise_frame = int((element.offset + element.duration.quarterLength) / quarter_note_duration * target_fps) + frame_start
                    piano_object.location.z = 0.0
                    piano_object.keyframe_insert(data_path="location", index=2, frame=rise_frame)

if __name__ == "__main__":
    musicxml_path = "C:\\xxx.mxl"  #please Insert your score path

    # オブジェクト名のプレフィックス
    object_prefix = ""

    # ターゲットのFPSを設定
    target_fps = 24  

    # キーフレームを設定
    set_keyframes_from_musicxml(musicxml_path, object_prefix, target_fps)


