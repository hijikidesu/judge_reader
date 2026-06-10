import cv2
import numpy as np
import time
import pandas as pd
from PIL import Image
import tensorflow as tf
import os

data_folder_path = r""

judge_data_folder_path = os.path.join(data_folder_path,"judge")

result_folder_path = os.path.join(data_folder_path,"judge_list")

judge_data_path = [f for f in os.listdir(judge_data_folder_path) if f.endswith('.mp4')] 

classes = ["0","1","2","3","4","5","6","7","8","9","-","+"] #判別したいラベル
num_classes = len(classes) #ラベルの数

try:
    model = tf.keras.models.load_model('judge_read_re_model.h5') # 保存されたモデルファイルを読み込む
except Exception as e:
    print("モデル読み込めんかったよ")
    print(e)


def image_crop(img,left,right,height): #画像を切り取る関数
    crop_area = (left, 0, right,height)

    # 画像を切り取る
    crop_img = img.crop(crop_area)

    crop_img = np.asarray(crop_img)

    #crop_img=cv2.resize(crop_img,(22,22))

    return crop_img


def extract_each_character(frame,judge_img_list): #画像から1文字ずつ抽出する関数
    
    (height, w) = frame.shape[:2] #画像の高さと長さを取得
    h_median = height/2 #高さの真ん中

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #グレースケール化
    
    # Cannyエッジ検出
    edges = cv2.Canny(frame, 120, 180)
    
    # 輪郭を検出
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  

    x_coords = []

    for contour in contours:
        y_coords_tmp =[]
        for j in range(len(contour)):
                y_coords_tmp.append(contour[j][0][1])
        y_coords_tmp = np.array(y_coords_tmp)  # numpy 配列に変換
        if  ((h_median-3 < y_coords_tmp) & (y_coords_tmp < h_median+3)).any():
            for s in range(len(contour)):
                x_coords.append(contour[s][0][0])

    if not x_coords:
        return

    far_right_x = np.max(x_coords)

    frame = Image.fromarray(frame)
    
    if far_right_x >88:
        
        #小数点以下の数字を取得
        first_decimal_place_number_right = far_right_x - 25
        first_decimal_place_number_left = far_right_x - 37

        first_decimal_place_number_image = image_crop(frame,first_decimal_place_number_left,first_decimal_place_number_right,height)

        #一の位の数字を取得
        one_place_number_right = far_right_x - 42
        one_place_number_left = far_right_x - 54

        one_place_number_image = image_crop(frame,one_place_number_left,one_place_number_right,height)

        #十の位の数字を取得
        tens_place_number_right = far_right_x - 56
        tens_place_number_left = far_right_x - 68

        tens_place_number_image= image_crop(frame,tens_place_number_left,tens_place_number_right,height)

        #百の位の数字を取得
        hundreds_place_number_right = far_right_x - 69
        hundreds_place_number_left = far_right_x - 81

        hundreds_place_number_image= image_crop(frame,hundreds_place_number_left,hundreds_place_number_right,height)
 
        #+か-かを取得
        symbol_right = far_right_x - 82
        symbol_left = far_right_x - 94

        symbol_image = image_crop(frame,symbol_left,symbol_right,height)

        img_number = 5
        judge_img_list.append(symbol_image) #+ or -
        judge_img_list.append(hundreds_place_number_image) #百の位
        judge_img_list.append(tens_place_number_image) #十の位
        judge_img_list.append(one_place_number_image) #一の位
        judge_img_list.append(first_decimal_place_number_image) #小数点以下
    
    elif 82<= far_right_x and  far_right_x < 89:
        
        #小数点以下の数字を取得
        first_decimal_place_number_right = far_right_x - 25
        first_decimal_place_number_left = far_right_x - 37

        first_decimal_place_number_image = image_crop(frame,first_decimal_place_number_left,first_decimal_place_number_right,height)

        #一の位の数字を取得
        one_place_number_right = far_right_x - 42
        one_place_number_left = far_right_x - 54

        one_place_number_image = image_crop(frame,one_place_number_left,one_place_number_right,height)

        #十の位の数字を取得
        tens_place_number_right = far_right_x - 56
        tens_place_number_left = far_right_x - 68

        tens_place_number_image= image_crop(frame,tens_place_number_left,tens_place_number_right,height)
    
        #+か-かを取得
        symbol_right = far_right_x - 69
        symbol_left = far_right_x - 81

        symbol_image = image_crop(frame,symbol_left,symbol_right,height)

        img_number = 4
        judge_img_list.append(symbol_image) #+ or -
        judge_img_list.append(tens_place_number_image) #十の位
        judge_img_list.append(one_place_number_image) #一の位
        judge_img_list.append(first_decimal_place_number_image) #小数点以下

    elif 73<= far_right_x and  far_right_x < 82:

        #小数点以下の数字を取得
        first_decimal_place_number_right = far_right_x - 25
        first_decimal_place_number_left = far_right_x - 37

        first_decimal_place_number_image= image_crop(frame,first_decimal_place_number_left,first_decimal_place_number_right,height)

        #一の位の数字を取得
        one_place_number_right = far_right_x - 42
        one_place_number_left = far_right_x - 54

        one_place_number_image= image_crop(frame,one_place_number_left,one_place_number_right,height)

        #+か-かを取得
        symbol_right = far_right_x - 55
        symbol_left = far_right_x - 67

        symbol_image= image_crop(frame,symbol_left,symbol_right,height)

        img_number = 3
        judge_img_list.append(symbol_image) #+ or -
        judge_img_list.append(one_place_number_image) #一の位
        judge_img_list.append(first_decimal_place_number_image) #小数点以下

    else:
        #print(f'{i}:うまく切り取れんかった')
        return

    return img_number


for movie_no,judge_movie in enumerate(judge_data_path):
    file_path = os.path.join(judge_data_folder_path, judge_movie)  # フルパスを作成
    music_name = judge_movie.replace('_judge.mp4', '')
    video = cv2.VideoCapture(file_path)

    # 動画情報の取得
    frameAll = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    framerate = video.get(cv2.CAP_PROP_FPS) # 動画フレームレートを取得

    judge_img_list = []

    img_number_list = []
    frame_list = []
    second_list = []

    start_time = time.time()


    #1フレームごとの画像をリストに
    for i in range(0,frameAll,1):
        ret, frame = video.read() # [ret]はread()の処理結果、[frame]は処理画像が格納される
    
    
        # フレームが正しく取得されているか確認
        if not ret:
            print(f"フレーム {i} の取得に失敗しました。")
            continue
        
        img_number = extract_each_character(frame,judge_img_list)

        if img_number is None:
            continue

        second = i/framerate
        img_number_list.append(img_number)
        frame_list.append(i)
        second_list.append(second)
        

    #print("画像読み込み完了!")

    judge_img_list = np.array(judge_img_list)
    judge_img_list = judge_img_list.astype("float") / 255

    judge_img_list = np.expand_dims(judge_img_list, axis=-1) 

    judge_prediction_list = model.predict(judge_img_list, verbose=0)
    judge_pre_list = tf.argmax(judge_prediction_list, axis=1)

    judge_list = []

    for count in range(len(img_number_list)):
        pop_judge = tf.slice(judge_pre_list, [0], [img_number_list[count]])  # スライスで必要な部分を取得
        # 残りの部分を更新
        judge_pre_list = tf.slice(judge_pre_list, [img_number_list[count]], [tf.size(judge_pre_list) - img_number_list[count]])
        pop_judge = pop_judge.numpy() # 出力のために .numpy() で変換

        judge = ""

        for l in range(len(pop_judge)):
                
            if l != len(pop_judge) -1:
                judge += classes[pop_judge[l]]
            
            else:
                judge += "." + classes[pop_judge[l]]

        judge_list.append(judge)

    former_judge = ''
    result_judge = []
    result_frame = []
    result_second = []
    result = pd.DataFrame() 

    for index,judge in enumerate(judge_list):
    
        skip_outer_loop = False  # フラグを初期化
    
        if judge[0] != '+' and judge[0] != '-': #最初がプラマイじゃない場合は追加しない
            continue

        for f in range(1,len(judge)):#数字のところにプラマイがあれば追加しない
            if f == len(judge)-2:
                continue
            
            if judge[f] == '+' or judge[f] == '-':
                skip_outer_loop = True  # フラグを設定
                break
            
        if skip_outer_loop: #あかんかったら追加しない
            continue     

        if former_judge != judge:
            result_judge.append(judge)
            result_frame.append(frame_list[index])
            result_second.append(second_list[index])
            former_judge = judge
        else:
            continue

    result['judge'] = result_judge
    result['frame'] = result_frame
    result['second'] = result_second

    csv_file_name = f"{music_name}_judge_list.csv"

    result.to_csv(os.path.join(result_folder_path, csv_file_name),index = False)
    print(f"{movie_no+1}データ目のcsvファイル出力完了！")

    video.release()  # 動画を解放する