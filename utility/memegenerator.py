import os
import sys
import logging
from PIL import Image, ImageDraw, ImageFont

def get_upper(somedata):
	'''
	Handle Python 2/3 differences in argv encoding
	'''
	result = ''
	try:
		result = somedata.decode("utf-8").upper()
	except:
		result = somedata.upper()
	return result

def get_lower(somedata):
	'''
	Handle Python 2/3 differences in argv encoding
	'''
	result = ''
	try:
		result = somedata.decode("utf-8").lower()
	except:
		result = somedata.lower()		

	return result

def make_meme(topString, topTextPosition, bottomString, bottomTextPosition, filename, logging):
    try:
        img = Image.open(filename)
    except Exception as e:
        logging.error(str(e))
        return False, "Failed to open image file."

    topString = get_lower(topString)
    bottomString = get_lower(bottomString)
    imageSize = img.size
    draw = ImageDraw.Draw(img)
    # find biggest font size that works
    fontSize = int(imageSize[1] / 8)
    font = ImageFont.truetype("./data/fonts/impact.ttf", fontSize)
    logofont = ImageFont.truetype("./data/fonts/ceribri.ttf", 12)
    # topTextSize = font.font.getsize(topString)
    # bottomTextSize = font.font.getsize(bottomString)

    # while topTextSize[0][0] > imageSize[0]-20 or bottomTextSize[0][0] > imageSize[0]-20:
    #     fontSize -= 1
    #     font = ImageFont.truetype("./data/fonts/impact.ttf", fontSize)
    #     topTextSize = font.font.getsize(topString)
    #     bottomTextSize = font.font.getsize(bottomString)
		

    # # find top centered position for top text
    # topTextPositionX = (imageSize[0] / 2) - (topTextSize[0][0] / 2)
    # topTextPositionY = 0
    # topTextPosition = (topTextPositionX, topTextPositionY)

    # # find bottom centered position for bottom text
    # bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0][0] / 2)
    # bottomTextPositionY = imageSize[1] - bottomTextSize[1][1]
    # bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

    # draw outlines
    outlineRange = int(fontSize / 15)
    for x in range(-outlineRange, outlineRange + 1):
        for y in range(-outlineRange, outlineRange + 1):
            draw.text((topTextPosition[0] + x, topTextPosition[1] + y), topString, (0, 0, 0), font=font)
            draw.text((bottomTextPosition[0] + x, bottomTextPosition[1] + y), bottomString, (0, 0, 0), font=font)

    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)

    logoTextPosition = (imageSize[0] - 80, imageSize[1] - 20)
    draw.text(logoTextPosition, "coinchance.io", (0, 0, 0), font=logofont)
	
    directory, file = os.path.split(filename)
    img_path = os.path.join('data', 'images', 'output', file)
    #img_path = "./data/temp/temp.png"
    img.save(img_path)
    return True, img_path

def make_meme2(topString, bottomString, filename, logging):
    try:
        img = Image.open(filename)
    except Exception as e:
        logging.error(str(e))
        return False, "Failed to open image file."

    topString = get_lower(topString)
    bottomString = get_lower(bottomString)
    imageSize = img.size
    draw = ImageDraw.Draw(img)
    # find biggest font size that works
    fontSize = int(imageSize[1] / 5)
    font = ImageFont.truetype("./data/fonts/impact.ttf", fontSize)
    logofont = ImageFont.truetype("./data/fonts/ceribri.ttf", 12)
    topTextSize = font.font.getsize(topString)
    bottomTextSize = font.font.getsize(bottomString)

    while topTextSize[0][0] > imageSize[0]-20 or bottomTextSize[0][0] > imageSize[0]-20:
        fontSize -= 1
        font = ImageFont.truetype("./data/fonts/impact.ttf", fontSize)
        topTextSize = font.font.getsize(topString)
        bottomTextSize = font.font.getsize(bottomString)
		

    # find top centered position for top text
    topTextPositionX = (imageSize[0] / 2) - (topTextSize[0][0] / 2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)

    # find bottom centered position for bottom text
    bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0][0] / 2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1][1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

    # draw outlines
    outlineRange = int(fontSize / 15)
    for x in range(-outlineRange, outlineRange + 1):
        for y in range(-outlineRange, outlineRange + 1):
            draw.text((topTextPosition[0] + x, topTextPosition[1] + y), topString, (0, 0, 0), font=font)
            draw.text((bottomTextPosition[0] + x, bottomTextPosition[1] + y), bottomString, (0, 0, 0), font=font)

    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)

    logoTextPosition = (imageSize[0] - 100, imageSize[1] - 30)
    draw.text(logoTextPosition, "coinchance.io", (255, 255, 255), font=logofont)
	
    directory, file = os.path.split(filename)
    img_path = os.path.join('images', 'output', file)
    #img_path = "./data/temp/temp.png"
    img.save(img_path)
    return True, img_path


# def make_meme(topString, bottomString, filename, logging):
# 	try:
# 		img = Image.open(filename)
# 	except Exception as e:
# 		logging.error(str(e))
# 		return False, None
# 	imageSize = img.size
# 	print(imageSize)
# 	draw = ImageDraw.Draw(img)
# 	# find biggest font size that works
# 	fontSize = int(imageSize[1]/5)
# 	font = ImageFont.truetype("./data/fonts/impact.ttf", fontSize)
# 	logofont = ImageFont.truetype("./data/fonts/ceribri.ttf", 12)
# 	topTextSize = font.font.getsize(topString)
# 	bottomTextSize = font.font.getsize(bottomString)

# 	while topTextSize[0][0] > imageSize[0]-20 or bottomTextSize[0][0] > imageSize[0]-20:
# 		fontSize = fontSize - 1
# 		font = ImageFont.truetype("./data/fonts/impact.ttf", fontSize)
# 		topTextSize = font.font.getsize(topString)
# 		bottomTextSize = font.font.getsize(bottomString)

# 	# find top centered position for top text
# 	topTextPositionX = (imageSize[0]/2) - (topTextSize[0][0]/2)
# 	topTextPositionY = 0
# 	topTextPosition = (topTextPositionX, topTextPositionY)

# 	# find bottom centered position for bottom text
# 	bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0][0]/2)
# 	bottomTextPositionY = imageSize[1] - bottomTextSize[1][1]
# 	bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

	

# 	# draw outlines
# 	# there may be a better way
# 	outlineRange = int(fontSize/15)
# 	for x in range(-outlineRange, outlineRange+1):
# 		for y in range(-outlineRange, outlineRange+1):
# 			draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
# 			draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)

# 	draw.text(topTextPosition, topString, (255,255,255), font=font)
# 	draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)

# 	logoTextPosition = (imageSize[0]-100, imageSize[1]-30)
# 	draw.text(logoTextPosition, "coinchance.io", (255,255,255), font=logofont)

# 	img.save("./data/temp/temp.png")
# 	return True, "./data/temp/temp.png"



if __name__ == '__main__':

	args_len = len(sys.argv)
	topString = ''
	meme = 'standard'

	if args_len == 1:
		# no args except the launch of the script
		bottomString = get_upper("Meme World")
		topString = get_upper("Hello")
		meme = get_lower("./meme_250675.png")
		 
		print('args plz')

	elif args_len == 2:
		# only one argument, use standard meme
		bottomString = get_upper(sys.argv[-1])

	elif args_len == 3:
		# args give meme and one line
		bottomString = get_upper(sys.argv[-1])
		meme = get_lower(sys.argv[1])

	elif args_len == 4:
		# args give meme and two lines
		topString = get_upper(sys.argv[-2])
		bottomString = get_upper(sys.argv[-1])
		meme = get_lower(sys.argv[1])
	else:
		# so many args
		# what do they mean
		# too intense
		print('to many argz')

	print(meme)	
	#filename = str(meme)+'.jpg'
	filename = str(meme)
	make_meme(topString, bottomString, filename)	
