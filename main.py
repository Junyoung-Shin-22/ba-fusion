import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import os
import sys
from tqdm import tqdm

if len(sys.argv) < 2:
    TARGET_NAME = input('제작할 학생의 이름 > ')
else:
    TARGET_NAME = sys.argv[1]

images = os.listdir('./student_portraits/')
names = [i.split('.')[0] for i in images]

print('loaded', len(names), 'students')
plt.rc('font', family='Malgun Gothic')

for k in range(1, len(TARGET_NAME)):
    left_chara = TARGET_NAME[:k]
    right_chara = TARGET_NAME[k:]

    left_idx = [
        i for i in range(len(names)) if names[i].split('(')[0].startswith(left_chara)
    ]
    right_idx = [
        i for i in range(len(names)) if names[i].split('(')[0].endswith(right_chara)
    ]

    print(f'We have {len(left_idx)} students starts with "{left_chara}"' ,[names[i] for i in left_idx])
    print(f'We have {len(right_idx)} students ends with "{right_chara}"', [names[i] for i in right_idx])

    if len(left_idx) == 0 or len(right_idx) == 0:
        print('skipping...')
        continue

    fig, axs = plt.subplots(len(left_idx), len(right_idx), figsize=(10, 10))
    
    if len(left_idx) == 1 and len(right_idx) == 1:
        axs = [[axs,],]
    elif len(left_idx) == 1:
        axs = [axs,]
    elif len(right_idx) == 1:
        for i in range(len(left_idx)):
            axs[i] = [axs[i],]

    fig.suptitle(f'{left_chara}/{right_chara}')

    os.makedirs(TARGET_NAME, exist_ok=True)

    for i, left in enumerate(tqdm(left_idx)):
        for j, right in enumerate(right_idx):
            im_left = np.array(Image.open(f'./student_portraits/{images[left]}').convert('RGB'))
            im_right = np.array(Image.open(f'./student_portraits/{images[right]}').convert('RGB'))

            im_new = im_left.copy()
            h, w, _ = im_new.shape

            im_new[:, w//2:, :] = im_right[:, w//2:, :]
            axs[i][j].imshow(im_new)

            axs[i][j].set_aspect('equal')
            axs[i][j].set_xticks([])
            axs[i][j].set_yticks([])
    
    fig.savefig(os.path.join(TARGET_NAME, f'{left_chara},{right_chara}.png'))