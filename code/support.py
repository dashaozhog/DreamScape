from os import walk
import pygame

def import_folder(path):
	surf_list = []
	for _,__,img_files in walk(path):
		for ass in img_files:
			fullpath = path + '/'+ ass
			asset = pygame.transform.scale(pygame.image.load(fullpath).convert_alpha(), (64,64))
			surf_list.append(asset)
	return surf_list