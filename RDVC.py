print('''--------------------------------------
|¯¯¯¯¯\   |¯¯¯¯\    |¯|   |¯|    /¯¯¯|
| |¯¯\ \  | |¯\ \   | |   | |   / /¯¯
| |__/ /  | |  | |  | |   | |  | |
|    _/   | |  | |  | |   | |  | |
| |\ \    | |  | |   \ \_/ /   | |
| | \ \   | |_/ /     \   /     \ \__
|_|  \_\  |____/       \_/       \___|
--------------------------------------''')
print("Rhythm Doctor Video Converter by 0x4D2\nversion release-1.0")
try:
    print("加载中...")
    import cv2 as c  # 视频处理
    import traceback  # 异常捕获
    import json  # JSOn
    from moviepy.editor import VideoFileClip  # 从视频中提取.mp3
    from pydub import AudioSegment  # 将.mp3转化为.ogg
    from tqdm import tqdm  # 进度条
    import zipfile  # 打包rdzip文件
    import os  # 文件处理
except ImportError:
    import pip
    print("检测到部分库未安装，正在安装库...")
    pip.main(["install", "--user", "opencv-python", "moviepy",
             "pydub", "tqdm", "ffmpeg-python"])  # 通过pip安装缺失的库
    import cv2 as c
    import traceback
    import json
    from moviepy.editor import VideoFileClip
    from pydub import AudioSegment
    from tqdm import tqdm
    import zipfile
    import os

decoration = []
shot = False

# 输入
vf = input("输入视频文件名>")
xi = input("输入生成视频的横向分辨率>")
yi = input("输入生成视频的纵向分辨率>")
song = input("输入音乐名称(留空默认为文件名)>")
artist = input("输入作曲家名称(留空默认为文件名)>")
pic = input("输入铺面预览图文件名(留空默认为视频第1帧)>")

# 处理
if not song:
    song = vf[:-4]
if not artist:
    artist = vf[:-4]
if not pic:
    pic = "preview.png"
    shot = True
else:
    try:
        f = open(pic, "r")
        f.close()
    except:
        print("预览图图片不存在，将使用视频第1帧作为预览图")
        pic = "preview.png"
        shot = True

setting = {"version": 54,
           "artist": artist,
           "song": song,
           "specialArtistType": "None",
           "artistPermission": "",
           "artistLinks": "",
           "author": "RDVC by 0x4D2",
           "difficulty": "Easy",
           "seizureWarning": False,
           "previewImage": pic,
           "syringeIcon": "",
           "previewSong": "",
           "previewSongStartTime": 0,
           "previewSongDuration": 10,
           "songNameHue": 0.05188763,
           "songLabelGrayscale": False,
           "description": "",
           "tags": "",
           "separate2PLevelFilename": "",
           "canBePlayedOn": "OnePlayerOnly",
           "firstBeatBehavior": "RunNormally",
           "multiplayerAppearance": "HorizontalStrips",
           "levelVolume": 1,
           "rankMaxMistakes": [20, 15, 10, 5],
           "rankDescription": ["你这个毫无希望的实习生！",  # F
                               "啊，你还可以做得更好",  # D
                               "嗯，勉强还成……",  # C
                               "咱们是黄金组合！",  # B
                               "你的表现真给力！",  # A
                               "惊艳绝伦的演出！！"]}  # S

try:  # 视频分辨率/颜色转化
    xi, yi = int(xi), int(yi)
    v = c.VideoCapture(vf)
    res = []
    fps = v.get(c.CAP_PROP_FPS)
    tf = int(v.get(c.CAP_PROP_FRAME_COUNT))
    fr = 0

    events = [{"bar": 1, "beat": 1, "y": 0, "type": "PlaySong", "filename": vf[:-4]+".mp3",
               "volume": 100, "pitch": 100, "pan": 0, "offset": 0, "bpm": fps*7.5, "loop": False}]

    print("转换视频中...")
    for i in tqdm(range(tf)):
        fr += 1
        f = []
        ret, frame = v.read()
        if frame is None:
            break
        if ret == True:
            rf = c.resize(frame, (xi, yi))
            for y in rf:
                x = []
                for a in y:
                    x.append(hex(a[2])[2:].zfill(2)+hex(a[1])
                             [2:].zfill(2)+hex(a[0])[2:].zfill(2))
                f.append(x)
            res.append(f)
        if i == 0 and shot:
            c.imwrite("preview.png", frame)

    # 提取音频
    print("提取音频中...")
    video = VideoFileClip(vf)
    audio = video.audio
    audio.write_audiofile(vf[:-4]+".mp3")

    # 转换为ogg
    #audio_ogg = AudioSegment.from_mp3(vf[:-4]+".mp3")
    #audio_ogg.export(vf[:-4]+".ogg", format="ogg")

    # 生成精灵
    print("生成精灵中...")
    with open("pixel.png", "wb+") as f:
        f.write(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1F\xF3\xFF\x61\x00\x00\x00\x01\x73\x52\x47\x42\x00\xAE\xCE\x1C\xE9\x00\x00\x00\x04\x67\x41\x4D\x41\x00\x00\xB1\x8F\x0B\xFC\x61\x05\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x12\x74\x00\x00\x12\x74\x01\xDE\x66\x1F\x78\x00\x00\x00\x22\x49\x44\x41\x54\x38\x4F\x63\x64\x60\x60\xF8\x0F\xC4\x64\x03\x26\x28\x4D\x36\x18\x35\x60\xD4\x00\x10\x18\x35\x60\xE0\x0D\x60\x60\x00\x00\x4D\x40\x01\x1F\x74\x3B\x2E\x9A\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82")

    # 生成铺面
    print("生成铺面中...")
    if xi/yi <= 16/9:
        s = 198 / yi
        sx = (352-s*xi+s) / 7.04
        sy = s / 3.96
    else:
        s = 352 / xi
        sx = s / 7.04
        sy = (198-s*yi+s) / 3.96
    scale = s / 16
    for x in range(xi):  # 352*198
        for y in range(yi):
            # 添加精灵
            decoration.append({"id": str(x*yi+y), "row": str(x*yi+y),
                              "rooms": [0], "filename": "pixel.png", "depth": 0, "visible": True})
            # 添加移动事件
            events.append({"bar": 1, "beat": 1, "type": "Move", "target": str(
                x*yi+y), "position": [sx+(s/3.52)*x, sy+(s/1.98)*y], "scale": [scale, scale], "duration": 0, "ease": "Linear"},)

    bar, beat, r = 1, 1, 0
    for i in tqdm(range(len(res))):  # 添加涂色事件
        for x in range(xi):
            for y in range(yi):
                if i != 0:
                    if res[i][yi-y-1][x] == res[i-1][yi-y-1][x]:
                        continue
                events.append({"bar": bar, "beat": beat, "type": "Tint", "target": str(x*yi+y), "border": "None", "borderColor": "FFFFFF",
                               "borderOpacity": 100, "opacity": 100, "tint": True, "tintColor": res[i][yi-y-1][x], "tintOpacity": 100},)

        beat += 0.125
        if beat >= 9:
            beat = 1
            bar += 1

    for x in range(xi):
        for y in range(yi):
            events.append({"bar": bar, "beat": beat, "type": "Tint", "target": str(x*yi+y), "border": "None", "borderColor": "FFFFFF",
                          "borderOpacity": 100, "opacity": 100, "tint": False, "tintColor": "FFFFFF", "tintOpacity": 100},)
    for i in range(3):
        events.append({"bar": bar+1+i, "beat": 1,
                      "y": 0, "type": "FinishLevel"})

    with open("main.rdlevel", "w", encoding="utf-8") as f:  # 写入.rdlevel文件
        # f.write(json.dumps(decoration))
        # f.write("\n")
        f.write(json.dumps({"settings": setting, "rows": [],
                "decorations": decoration, "events": events}))

    print("打包rdzip文件中...")
    rdzip = zipfile.ZipFile(vf[:-4]+".rdzip", mode="w")
    rdzip.write("main.rdlevel")
    rdzip.write("pixel.png")
    rdzip.write(vf[:-4]+".mp3")
    rdzip.write(pic)
    rdzip.close()
    os.remove("main.rdlevel")
    os.remove("pixel.png")
    os.remove(vf[:-4]+".mp3")
    if shot:
        os.remove(pic)
except:
    print("\n程序出现错误，报错信息如下：\n"+"-"*30)
    traceback.print_exc()
else:
    print("完成")
finally:
    input("按回车继续...")
