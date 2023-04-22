# ==============================================================
# 0. 라이브러리 불러오기
# ==============================================================
import os
import argparse

# ==============================================================
# 0. 변수 정의
# ==============================================================
parser = argparse.ArgumentParser(description='3_Front_Similar_Name_Image_Remove')

parser.add_argument('--base-path', default='/media/hi/SK Gold P31/Capstone/GolfBall/Golfball_Near_Test', type=str, help='데이터셋이 모여있는 grandmother 폴더 경로 지정')
parser.add_argument('--filename-split-criterions', default=['_jpeg', '_JPEG', '_png', '_jpg'], type=str, nargs='*', help='이미지명 Split 기준')

parser.add_argument('--source-parent-pathes', default=['images'], type=str, nargs='*', help='데이터셋의 이미지가 모여있는 mother 폴더 지정')
parser.add_argument('--source-child-pathes', default=['train', 'val', 'test'], type=str, nargs='*', help='데이터셋의 이미지가 모여있는 child 폴더 지정')

parser.add_argument('--image-folder', default='images', type=str, help='base_path/source_parent_pathes/source_child_pathes에서 이미지가 모여있는 source_parent_pathes 폴더명')
parser.add_argument('--label-folder', default='labels', type=str, help='base_path/source_parent_pathes/source_child_pathes에서 라벨이 모여있는 source_parent_pathes 폴더명')
parser.add_argument('--before-file-extension', default='.jpg', type=str, help='base_path/image_folder/source_child_pathes 안에 들어있는 이미지 파일 확장자')
parser.add_argument('--after-file-extension', default='.txt', type=str, help='base_path/label_folder/source_child_pathes 에서 오픈할 텍스트 파일 확장자')

args = parser.parse_args()

dup_images_idx = {}

def get_filenames(folder_path):
    filenames = os.listdir(folder_path)
    return filenames

def Remove_Image(base_path):
    # --------------------------------------------------------------
    # 0) 변수 정의
    # --------------------------------------------------------------
    global dup_images_idx

    # --------------------------------------------------------------
    # 1) Image File list 불러오기
    # --------------------------------------------------------------
    for image_path in args.source_parent_pathes:
        for train_path in args.source_child_pathes:
            image_filenames = get_filenames(f'{base_path}/{image_path}/{train_path}')
            image_filenames.sort()
            """
            print("image_filenames : ", image_filenames)
            """

            # --------------------------------------------------------------
            # (1) 이미지 파일 중에서, Split 기준에 부합하는 string을 포함한 경우만 진행
            # --------------------------------------------------------------
            for idx in range(len(image_filenames)-1):
                for filename_split_criterion in args.filename_split_criterions:
                    if image_filenames[idx].find(filename_split_criterion) != -1:
                        # 1] 이미지 파일명 + 경로 + 용량 추출
                        now_image_filename, next_image_filename = image_filenames[idx], image_filenames[idx+1]
                        next_image_path = f'{base_path}/{args.image_folder}/{train_path}/{next_image_filename}'
                        next_image_filesize = os.path.getsize(next_image_path)

                        # 2] Split한 이미지명이 다음 이미지와 같은 경우 and 마지막 idx-2가 아닌 경우 : [list에 다음 이미지 index + 파일 용량 저장]
                        if now_image_filename[0:now_image_filename.find(filename_split_criterion)] == next_image_filename[0:next_image_filename.find(filename_split_criterion)] and idx < len(image_filenames)-2:
                            # [1] 처음 idx인 경우 : list에 무조건 현재 이미지 index + 파일 용량 저장
                            if idx == 0:
                                now_image_path = f'{base_path}/{args.image_folder}/{train_path}/{now_image_filename}'
                                now_image_filesize = os.path.getsize(now_image_path)
                                dup_images_idx = {}
                                dup_images_idx[idx] = now_image_filesize

                        # 3] Split한 이미지명이 다음 이미지와 다른 경우 or 마지막 idx-2인 경우
                        else:
                            # [1] list에 원소 있는 경우 : [list에 이미지 파일 용량 + index 저장] + 파일 지우기 + list 비우기
                            if len(dup_images_idx) != 0:
                                # 1]] 마지막 idx-2인 경우 : list에 다음 이미지 index + 파일 용량 저장
                                if idx >= len(image_filenames)-2:
                                    dup_images_idx[idx + 1] = next_image_filesize

                                # 2]] 최대 용량 파일 제외한 모든 파일 지우기
                                """
                                print("dup_images_idx : ", dup_images_idx)
                                print("max(dup_images_idx, key=dup_images_idx.get) : ", max(dup_images_idx, key=dup_images_idx.get))
                                """
                                dup_images_idx.pop(max(dup_images_idx, key=dup_images_idx.get))
                                """
                                print("dup_images_idx : ", dup_images_idx)
                                """
                                for dup_image_idx in dup_images_idx.keys():
                                    remove_image_path = f'{args.base_path}/{args.image_folder}/{train_path}/{image_filenames[dup_image_idx]}'
                                    remove_label_path = f'{args.base_path}/{args.label_folder}/{train_path}/{image_filenames[dup_image_idx].replace(args.before_file_extension, args.after_file_extension)}'

                                    print(f"remove_image_path : {remove_image_path}")
                                    print(f"remove_label_path : {remove_label_path}")

                                    os.unlink(remove_image_path)
                                    os.unlink(remove_label_path)

                                # 3]] list 비우기
                                dup_images_idx = {}
                            # [2] list에 원소 없는 경우 : 건너띄기
                            else:
                                pass

                        # 4] 모든 경우 : list에 다음 이미지 index + 파일 용량 저장
                        dup_images_idx[idx + 1] = next_image_filesize

                        # 5] 탈출
                        break


Remove_Image(args.base_path)