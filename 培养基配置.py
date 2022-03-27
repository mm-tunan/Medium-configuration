###培养基配方
###第一步创建配置文件（也就是培养基的配方）


import easygui as g
import time
import re
import os


# 创建培养基配置函数
def ms_creat():
    now_time = time.strftime("%Y-%m-%d", time.localtime())
    print(now_time)
    # ms_file = open(now_time,mode="w")
    ms_content = g.enterbox(msg="请用空格分隔\n例:蔗糖 琼脂 MS粉", title="培养基组分")
    # print(ms_content)
    ms_list = ms_content.split(" ")
    # print(ms_list)
    ms_contents = g.multenterbox(msg="根据提示输入终浓度,\n固体单位g/L,溶液单位mg/L或mol/L", title="终浓度", fields=ms_list)
    # print(ms_contents)
    ms_contents_quantity = g.multenterbox(msg="注意单位!!!\n激素和抗生素单位mg/ml", title="母液浓度", fields=ms_list)
    # print(ms_contents_quantity)
    ms_contents_M = g.multenterbox(msg="注意单位!!!\n激素和抗生素单位M", title="母液浓度", fields=ms_list)
    # 将输入的数据进行整理，保存为字典
    num = 0
    ms_dict = {}
    for conts in ms_list:
        midu_list = []
        midu_list.append(ms_contents[num])
        midu_list.append(ms_contents_quantity[num])
        midu_list.append(ms_contents_M[num])
        ms_dict[conts] = midu_list
        num = num + 1
    # print(ms_dict)

    # 将字典保存为txt文档作为配置文件，并可以直接修改
    list_dir = os.listdir()
    if "配方" not in list_dir:
        os.mkdir("配方")
        os.chdir("./配方")
    else:
        print("配方文件已存在")
        os.chdir("./配方")
    file_name = g.enterbox(msg="培养基名", title="可以不写，不写默认为时间")
    if file_name == "":
        ms_file = open(f"{now_time}.txt", mode="w", encoding="UTF-8")
    else:
        ms_file = open(f"{file_name}.txt", mode="w", encoding="UTF-8")

    ms_file.write("名称\t单位（mg/ml）或（M）\t单位（mg/L）\t单位（M）\n")
    for conts_key in ms_dict:
        ms_file.write(f"{conts_key}\t{ms_dict[conts_key][0]}\t{ms_dict[conts_key][1]}\t{ms_dict[conts_key][2]}\n")
    ms_file.close()
    os.chdir("../")

# 使用创建好的配置文件函数：
def ms_use(ml):
    # ml = 100
    os.chdir("./配方")
    file_list = os.listdir()
    if len(file_list) == 0:
        g.msgbox("请创建配置文件")
    elif len(file_list) == 1:
        ms_file = open(file_list[0], mode="r", encoding="UTF-8")
    elif len(file_list) >= 1:
        # print(file_list)
        ms_choice = g.choicebox(choices=file_list)
        ms_file = open(ms_choice, mode="r", encoding="UTF-8")
        # print(ms_file)
    ##创建的ms培养基文本对象再反读为字典形式，方便后期使用
    ms_dict = {}
    for line in ms_file:
        # print(line)
        if "名称" in line:
            continue
        if line == "\n":
            exit("ok")
        else:
            # line = line.strip()
            line_list = line.split("\t")
            # print(line_list)
            line_list[-1] = line_list[-1].strip()
            # print(line_list)
            if len(line_list) == 4:
                ms_dict[line_list[0]] = line_list[1:4]
            elif len(line_list) == 2:
                ms_dict[line_list[0]] = [line_list[1]]
                ms_dict[line_list[0]].append("")
                ms_dict[line_list[0]].append("")
            elif len(line_list) == 3:
                ms_dict[line_list[0]] = line_list[1:3]
                ms_dict[line_list[0]].append("")
    # print(ms_dict)


    # print(ms_dict)
    os.chdir("../")


    ##计算各组分用量和浓度并保存在字典中
    ##第一部分
    ms_use_dict = {}
    for k in ms_dict:
        if ms_dict[k][1] == '' and ms_dict[k][2] == '':
            ms_use_dict[k] = str(round(float(ms_dict[k][0]) / 1000 * ml, 3)) + " g"
        # print(ms_use_dict)
        elif ms_dict[k][2] == '':
            ms_use_dict[k] = str(round(float(ms_dict[k][0]) * ml / float(ms_dict[k][1]), 3)) + " ul"
        # print(ms_use_dict)
        elif ms_dict[k][1] == '':
            ms_use_dict[k] = str(round(float(ms_dict[k][0]) * ml / float(ms_dict[k][2]) * 1000, 3)) + " ul"
    # print(ms_use_dict)
    return ms_use_dict


# 将培养基配方打印出来，方便确认
# 需要输入上一个函数生成的字典，以及使用多少ml
def ms_confirm(ms_use_dict, ml):
    log_dir = os.listdir()
    # print(ms_use_dict)
    ms_use_file = open("ms_log.txt", mode="w", encoding="UTF-8")
    ms_use_file.write(time.strftime("%Y-%m-%d %X", time.localtime()))
    ms_use_file.write("\n")
    ms_use_file.write("试剂名称\t所需用量\n")
    for k in ms_use_dict:
        ms_use_file.write(f"{k}\t{ms_use_dict[k]}\n")
    # ms_use_file.write(f"{ml}")
    ms_use_file.write("pH 6.0 \t 请根据实验室实际水质情况而定而定\n")
    ms_use_file.write(f"备注：{ml}培养基将用于:")
    ms_use_file.write("\n")
    ms_use_file.close()
    ms_log_file = open("ms_log.txt", mode="r", encoding="UTF-8")
    last_file_content = g.textbox(msg="确认试剂", text=ms_log_file.read(), codebox=True)
    last_file = open("ms试验记录.txt", mode="a", encoding="UTF-8")
    for line in last_file_content:
        last_file.write(line)
    last_file.write("\n")
    last_file.close()


def main():
    title = g.msgbox(msg="培养基配置", title="确认配置？", ok_button="配?不配!")
    while 1:
        ms_choice = g.buttonbox(msg="流程选择", title="选择", choices=("创建配置文件", "修改配置文件", "使用配置文件", "我不配"))
        if ms_choice == "创建配置文件":
            ms_creat()
            g.msgbox("配置文件已创建")
        elif ms_choice == "修改配置文件":
            now_time = time.strftime("%Y-%m-%d", time.localtime())
            os.chdir("./配方")
            file_list = os.listdir()
            # print(file_list)
            if len(file_list) == 0:
                g.msgbox("请创建配置文件")
            elif len(file_list) == 1:
                ms_file = open(file_list[0], mode="r", encoding="UTF-8")
                ms_file_revise = g.textbox(msg="修改配方", title="直接修改，不要修改\\t的位置", text=ms_file, codebox=True)
                new_name = g.enterbox(title="请输入新名字")
                if new_name != "":
                    ms_new_file = open(f"{new_name}.txt", mode="w", encoding="UTF-8")
                else:
                    ms_new_file = open(f"{new_name}.txt", mode="w", encoding="UTF-8")
                # ms_new_file.write(time.strftime("%Y-%m-%d %X", time.localtime()))
                # ms_file_revise = g.textbox(msg="修改配方", title="直接修改，不要修改\\t的位置", text=ms_file, codebox=True)
                for line in ms_file_revise:
                    ms_new_file.write(line)
                # ms_new_file.write("\n")
                ms_new_file.close()
            elif len(file_list) >= 1:
                ms_choice = g.choicebox(choices=file_list)
                # print(ms_choice)
                ms_file = open(ms_choice, mode="r", encoding="UTF-8")
                ms_file_revise = g.textbox(msg="修改配方", title="直接修改，不要修改\\t的位置", text=ms_file, codebox=True)
                # print(ms_file_revise)
                new_name = g.enterbox(title="请输入新名字")
                if new_name != "":
                    ms_new_file = open(f"{new_name}.txt", mode="w", encoding="UTF-8")
                else:
                    ms_new_file = open(f"{now_time}.txt", mode="w", encoding="UTF-8")

                # ms_new_file.write(time.strftime("%Y-%m-%d %X", time.localtime()))
                for line in ms_file_revise:
                    ms_new_file.write(line)
                # ms_new_file.write("\n")
                ms_new_file.close()
            os.chdir("../")


        elif ms_choice == "使用配置文件":
            ml = g.enterbox(msg="输入配多少ml MS培养基", title="预期体积")
            ml = float(ml)
            ms_use_dict = ms_use(ml)
            ms_confirm(ms_use_dict, ml)
        elif ms_choice == "我不配":
            g.msgbox(msg="退出", title="退出", ok_button="退下吧")
            g.msgbox("真不匹配?", ok_button="不配？")
            exit("欢迎下次使用")


if __name__ == "__main__":
    main()
