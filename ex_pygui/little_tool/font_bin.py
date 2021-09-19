def font_2_bin_zimo3(filepath, filepath1):
    global font_xsize, font_ysize, bytesline, word, unicode_word

    save_file = open(filepath1, "w+")
    s = "#include \"all_font_map.h\"\n"
    save_file.write(s)
    s = "static const all_font_map_struct all_font_map[] = \n"
    save_file.write(s)
    s = "{\n"
    save_file.write(s)
    # sf = open(filepath, "r")
    i = 1
    word_offset = 0
    with open(filepath, "r") as sf:
        data = sf.readline()
        while data:
            # print(data)
            word_array = data.split(' ')
            # print(word_array)
            if len(word_array) == 3:
                word = word_array[1]
                try:
                    unicode_word = ord(word)
                except:
                    data = sf.readline()
                    continue
                # print("%04x" % (unicode_word))
                i += 1
                while i != unicode_word:
                    s = "\t{  0,  0, 0xFFFFFFFF},\n"
                    save_file.write(s)
                    i += 1
                if i == unicode_word:
                    while True:
                        data = sf.readline()
                        data_array = data.split(',')
                        # print(data_array)
                        if len(data_array) == 5:
                            # print(data_array)
                            font_xsize = int(data_array[0].split('x')[1], 16)
                            font_ysize = int(data_array[1].split('x')[1], 16)
                            bytesline = int(data_array[2].split('x')[1], 16)
                            # print(font_xsize, bytesline)
                            s = "\t{%3d,%3d, 0x%08x},/* 0x%04x */\n" % (font_xsize, bytesline, word_offset, unicode_word)
                            save_file.write(s)
                            break
                word_offset += font_xsize * font_ysize // 8
            data = sf.readline()

        s = "};\n"
        save_file.write(s)
        s = "\nconst all_font_map_struct *p_all_font_map = all_font_map;\n"
        save_file.write(s)
        s = "const unsigned int all_font_map_size = sizeof(all_font_map)/sizeof(all_font_map[0]);\n"
        save_file.write(s)

        save_file.close()
        sf.close()

def font_2_bin_fontconvert(filepath, filepath1):
    global font_xsize, font_ysize, bytesline, word, unicode_word, width

    save_file = open(filepath1, "w+")
    s = "#include \"all_font_map.h\"\n"
    save_file.write(s)
    s = "static const all_font_map_struct all_font_map[] = \n"
    save_file.write(s)
    s = "{\n"
    save_file.write(s)
    i = 1
    word_offset = 0
    with open(filepath, "r") as sf:
        while True:
            data = sf.readline()
            if "GUI_CONST_STORAGE GUI_CHARINFO_EXT" in data:
                break
        data = sf.readline()
        while "};" not in data:
            word_array = data.split(',')
            # print(word_array)
            font_xsize = int(word_array[1].split('{')[1])
            bytesline = (int(word_array[5])+7)//8
            font_ysize = int(word_array[2])
            width = int(word_array[5])
            word = word_array[6].split(' ') #data.split(' ')
            # print(word)
            unicode_word = int(word[5].split(',')[0], 16)
            i += 1
            while i != unicode_word:
                s = "\t{  0,  0, 0xFFFFFFFF},\n"
                save_file.write(s)
                i += 1
            if i == unicode_word:
                s = "\t{%3d,%3d, 0x%08x},/* 0x%04x */\n" % (width, bytesline, word_offset, unicode_word)
                save_file.write(s)
            word_offset += font_xsize*font_ysize//8
            data = sf.readline()

        s = "};\n"
        save_file.write(s)
        s = "\nconst all_font_map_struct *p_all_font_map = all_font_map;\n"
        save_file.write(s)
        s = "const unsigned int all_font_map_size = sizeof(all_font_map)/sizeof(all_font_map[0]);\n"
        save_file.write(s)

        save_file.close()
        sf.close()


if __name__ == '__main__':
    filepath = "D:/new_song_36x36_map.c"
    filepath1 = "D:/new_song_36x36_map1.c"
    font_2_bin_zimo3(filepath, filepath1)
    # filepath = "C:/Users/Administrator/Desktop/black36.c"
    # filepath1 = "D:/new_song_36x36_map1.c"
    # font_2_bin_fontconvert(filepath, filepath1)
