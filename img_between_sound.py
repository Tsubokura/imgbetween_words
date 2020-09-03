from argwords2vec import generate_vector
from generate_sounds import generate_sounds
import sys

def main():
    img_name = 'motet_womanwithamblera.jpeg'
    imgsdir_name = './imgs/'

    args_list = sys.argv
    del args_list[0]
    # args_list = ['綺麗', 'かわいい', 'あざやか']
    print(args_list)
    vector_fromwords = generate_vector(args_list)
    generate_sounds(vector_fromwords, imgsdir_name + img_name)

if __name__ == "__main__":
    main()
