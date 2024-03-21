# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:24:47 2024

@author: Daniel Hodgins
"""
import numpy as np
from PIL import Image, ImageDraw
import time

REGION_SIZE = 16  # Adjust the region size as needed

# Load reference images for digits 0 through 9, lowercase letters, and uppercase letters
reference_images = {}
for i in range(8):
    reference_images[str(i)] = Image.open(f"Thesis edge counter/symbol_{i}.png").convert("L")


# Convert reference images to grayscale
reference_images_gray = {}
for char, ref_img in reference_images.items():
    reference_images_gray[char] = np.array(ref_img)  # Convert grayscale image to numpy array

# Precompute rotated reference images
rotated_reference_images = {}
for char, ref_img in reference_images_gray.items():
    rotated_reference_images[char] = [Image.fromarray(np.uint8(ref_img)).rotate(angle) for angle in [0, 90, 180, 270]]

start=time.time()

# Function to compare a region with reference images and determine the most similar character and its index
def compare_region(region):
    best_match = None
    best_match_index = None
    min_diff = float('inf')
    value = 0  # Initialize value here
    for i, (char, ref_img_rotated_list) in enumerate(rotated_reference_images.items()):
        for ref_img_rotated in ref_img_rotated_list:
            diff = np.sum(np.abs(region - np.array(ref_img_rotated)))
            if diff < min_diff:
                min_diff = diff
                best_match_index = i
    # Assign value based on best_match_index after the loop
    if best_match_index == 0:
        value = 0
    elif best_match_index == 1:
        value = 0.5
    elif best_match_index == 2 or best_match_index == 3 or best_match_index == 6 or best_match_index == 7: #deg2 or edge
        value = 1
    elif best_match_index == 4: #deg3
        value = 1.5
        #print("hi4")
    elif best_match_index == 5: #deg4
        value = 2
        #print("hi5")
    return value

    
def edge_sum(image_path):
    es=0 #set initial edge sum to 0
    # Open the image
    img = Image.open(image_path).convert("L")
    width, height = img.size
    # Iterate over regions
    for x in range(0, width, REGION_SIZE):
        for y in range(0, height, REGION_SIZE):
            # Extract region
            region = np.array(img.crop((x, y, x+REGION_SIZE, y+REGION_SIZE)))
            # Compare region with reference images to determine the most similar character
            es=es+compare_region(region)  
    return es

# Example usage
image_path = "prism9.png"
print("edgesum(prism3)=", edge_sum("prism3.png")) 
#print(round(time.time()-start,2),"seconds")
print("edgesum(prism4)=", edge_sum("prism4.png"))
#print(round(time.time()-start,2),"seconds")
print("edgesum(prism5)=", edge_sum("prism5.png")) 
#print(round(time.time()-start,2),"seconds")
print("edgesum(prism6)=", edge_sum("prism6.png"))
#print(round(time.time()-start,2),"seconds")
print("edgesum(prism7)=", edge_sum("prism7.png")) 
#print(round(time.time()-start,2),"seconds")
print("edgesum(prism8)=", edge_sum("prism8.png"))
#print(round(time.time()-start,2),"seconds")
print("edgesum(prism9)=", edge_sum("prism9.png")) 
#print(round(time.time()-start,2),"seconds")

print(round(time.time() - start, 2), "seconds")
print(round(time.time()-start,2),"seconds")




