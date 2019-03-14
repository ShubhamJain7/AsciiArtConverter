import argparse
import os
import sys
from PIL import Image,ImageDraw,ImageChops

Image.MAX_IMAGE_PIXELS = 1000000000 
ASCII_CHARS = ['@@','##','SS','%%','??','**','++',';;','::',',,','  ']

def get_args():
	parser = argparse.ArgumentParser(description="Convert images to ASCII art")
	parser.add_argument('image_path', type=str, action='store', help='Path to image')
	parser.add_argument('--save_dir', type=str, action='store', help='Path to store results', default='./')
	parser.add_argument('--save_name', type=str, action='store', help='Name of result', default='ascii_art')
	parser.add_argument('--result_type', type=int, action='store', help="0 convert to image, 1 convert to text file, 2 convert to image and text file", default=0)
	parser.add_argument('--contrast', type=int, action='store', help='Intensity of contrast to be applied', default=100)
	return parser.parse_args()

def change_contrast(img, level):
	factor = (259 * (level + 255)) / (255 * (259 - level))
	def contrast(c):
		return 128 + factor * (c - 128)
	return img.point(contrast)

def get_ascii(image, width):
	initial_pixels = list(image.getdata())
	new_pixels = [ASCII_CHARS[pixel_value // 25] for pixel_value in initial_pixels]
	pixels =  ''.join(new_pixels)
	len_pixels = len(pixels)
	new_image = [pixels[index:index+(width*2)] for index in range(0, len_pixels, (width*2))]
	final = '\n'.join(new_image)
	return final

def trim(img):
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)

def save_image(ascii, path):
	img = Image.new('RGB', (10000,15000) ,color=(255,255,255))
	d = ImageDraw.Draw(img)
	d.text((20, 20), ascii , fill=(0, 0, 0))
	del d
	img = trim(img)
	img.save(path)

def save_text(ascii, path):
	f = open(path,'w')
	f.write(ascii)
	f.close()

def check_save_file(save_dir,save_name):
		path = os.path.join(save_dir,save_name)
		if os.path.exists(path):
			print("ERROR: A file with the same name as result already exists!")
			sys.exit()

def main():

	args = get_args()
	image_path = args.image_path
	save_dir = args.save_dir
	save_name = args.save_name
	result_type = args.result_type
	contrast = args.contrast

	if not os.path.exists(image_path):
		print("ERROR: Path to image is incorrect!")
		sys.exit()

	if not os.path.exists(save_dir):
		os.makedirs(save_dir)

	image = Image.open(image_path).convert('L')
	size = image.size
	width, height = size[0]//2 , size[1]//2
	image = image.resize((width,height))
	image = change_contrast(image,contrast)
	ascii = get_ascii(image, width)

	if result_type==0:
		check_save_file(save_dir,save_name+".png")
		path = os.path.join(save_dir,save_name+".png")
		save_image(ascii,path)

	elif result_type==1:
		check_save_file(save_dir,save_name+".txt")
		path = os.path.join(save_dir,save_name+".txt")
		save_text(ascii,path)

	elif result_type==2:
		check_save_file(save_dir,save_name+".png")
		path = os.path.join(save_dir,save_name+".png")
		save_image(ascii,path)
		check_save_file(save_dir,save_name+".txt")
		path = os.path.join(save_dir,save_name+".txt")
		save_text(ascii,path)
	
if __name__ == '__main__':
	main()