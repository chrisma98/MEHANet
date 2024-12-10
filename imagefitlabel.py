import SimpleITK as sitk
import os


def align_images(input_image_path, input_label_path, output_image_path, output_label_path):
    # 读取图像和标签文件
    print("开始读取 NIfTI 文件...")
    image = sitk.ReadImage(input_image_path)
    label = sitk.ReadImage(input_label_path)
    print("NIfTI 文件读取完成。")

    # 获取原始图像和标签文件的尺寸
    image_size = image.GetSize()
    label_size = label.GetSize()
    print(f"原始图像尺寸: {image_size}")
    print(f"原始标签尺寸: {label_size}")

    # 对齐图像和标签文件的空间尺寸
    if image_size != label_size:
        print("对齐图像和标签文件的空间尺寸...")
        reference_image = image if image_size > label_size else label

        # 使用Resample函数调整尺寸
        transform = sitk.Transform()
        interpolator = sitk.sitkLinear
        default_value = 0
        resampled_image = sitk.Resample(image, reference_image, transform, interpolator, default_value)
        resampled_label = sitk.Resample(label, reference_image, transform, sitk.sitkNearestNeighbor, default_value)

        # 保存对齐后的图像和标签文件
        print("保存对齐后的图像和标签文件...")
        sitk.WriteImage(resampled_image, output_image_path)
        sitk.WriteImage(resampled_label, output_label_path)
    else:
        # 如果尺寸已经相同，则直接保存原始文件
        print("图像和标签文件尺寸相同，无需对齐...")
        sitk.WriteImage(image, output_image_path)
        sitk.WriteImage(label, output_label_path)


# 定义输入和输出文件夹路径
input_image_folder = '/home/bob/new-finish/image'
input_label_folder = '/home/bob/new-finish/label1'
output_image_folder = '/home/bob/new-finish/image1'
output_label_folder = '/home/bob/new-finish/label2'

# 确保输出文件夹存在
if not os.path.exists(output_image_folder):
    os.makedirs(output_image_folder)
if not os.path.exists(output_label_folder):
    os.makedirs(output_label_folder)

# 遍历文件夹中的所有文件
for filename in os.listdir(input_label_folder):
    print(filename[0:8])
    if filename.endswith('.nii.gz'):
        input_image = os.path.join(input_image_folder, filename)
        print(input_image)
        input_label = os.path.join(input_label_folder, filename)
        output_image = os.path.join(output_image_folder, filename[0:8]+'_0000'+".nii.gz")
        output_label = os.path.join(output_label_folder, filename)

        # 对齐并保存文件
        align_images(input_image, input_label, output_image, output_label)

print("所有文件对齐完成。")