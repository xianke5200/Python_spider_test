import xlwt
import time

workbook = xlwt.Workbook()
mySheet = workbook.add_sheet('动态心率解析数据')
mySheet1 = workbook.add_sheet('心率带解析数据')

mySheet.write(0, 0, '序号')
mySheet.write(0, 1, 'ppg数据')
mySheet.write(0, 2, 'pre数据')
mySheet.write(0, 3, 'ps数据')
mySheet.write(0, 4, 'curr数据')
mySheet.write(0, 5, 'env数据')
mySheet.write(0, 6, 'X')
mySheet.write(0, 7, 'Y')
mySheet.write(0, 8, 'Z')
mySheet.write(0, 9, '心率')

mySheet1.write(0, 0, '心率')

def hr_data_parse(filename):
    index = 0
    with open(filename, 'rb') as hr_file:
        data = hr_file.readline()
        while data:
            if "(0x)" in data.decode():
                res = data.decode().split("(0x)", 1)
                if(len(res[1]) >= 18):
                    temp = res[1].replace('\n','')
                    hr_data = temp.split('-')
                    # print(hr_data)
                    spo2_len = len(hr_data)
                    hr_data = hr_data[0:(spo2_len-1)]
                    for i in range(spo2_len-1):
                        if (i % 6) == 0:
                            index = index + 1
                        mySheet.write(index, i%6, hr_data[i])

                    # cnt = int(hr_data[17], 16)
                    # ppg_data = (int(hr_data[0], 16) << 8) | int(hr_data[1], 16)
                    # pre_data = (int(hr_data[2], 16) << 8) | int(hr_data[3], 16)
                    # ps_data = (int(hr_data[4], 16) << 8) | int(hr_data[5], 16)
                    # curr_data = (int(hr_data[6], 16) << 8) | int(hr_data[7], 16)
                    # env_data = (int(hr_data[8], 16) << 8) | int(hr_data[9], 16)
                    #
                    # x_data = (int(hr_data[10], 16) << 8) | int(hr_data[11], 16)
                    # if int(hr_data[10], 16) & 0x80 == 0x80:
                    #     x_data = -(65535-x_data + 1)
                    #
                    # y_data = (int(hr_data[12], 16) << 8) | int(hr_data[13], 16)
                    # if int(hr_data[12], 16) & 0x80 == 0x80:
                    #     y_data = -(65535-y_data + 1)
                    #
                    # z_data = (int(hr_data[14], 16) << 8) | int(hr_data[15], 16)
                    # if int(hr_data[14], 16) & 0x80 == 0x80:
                    #     z_data = -(65535-z_data + 1)
                    # hr = int(hr_data[16], 16)

                    # index = index + 1
                    # mySheet.write(index, 0, cnt)
                    # mySheet.write(index, 1, ppg_data)
                    # mySheet.write(index, 2, pre_data)
                    # mySheet.write(index, 3, ps_data)
                    # mySheet.write(index, 4, curr_data)
                    # mySheet.write(index, 5, env_data)
                    # mySheet.write(index, 6, x_data)
                    # mySheet.write(index, 7, y_data)
                    # mySheet.write(index, 8, z_data)
                    # mySheet.write(index, 9, hr)

            data = hr_file.readline()

def polar_h10_data_parse(filename):
    index = 0
    with open(filename, 'rb') as hr_file:
        data = hr_file.readline()
        while data:
            if "Heart Rate Measurement" in data.decode():
                res = data.decode().split(" ")
                hr_data = int(res[3])
                # print(hr_data)

                index = index + 1
                mySheet1.write(index, 0, hr_data)

            data = hr_file.readline()


if __name__ == '__main__':
    file_name = "2.txt"
    hr_data_parse(file_name)
    # file_name1 = "Polar H10-1126.txt"
    # polar_h10_data_parse(file_name1)

    now = time.localtime()
    workbook.save('心率数据解析' + '%s%s%s%s%s%s' % (
    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec) + '.xls')