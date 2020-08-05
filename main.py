import WeiBanAPI
import json
import time  # time.sleep延时
import os  # 兼容文件系统
import random

tenantCode = '61050002'  # 成电ID

def main():
    # 显示License
    licenseFile = open('.' + os.sep + 'LICENSE', encoding='utf-8')
    print(licenseFile.read())
    licenseFile.close()

    # 登录

    # 补打空cookie
    cookie = ''

    loginResponse = WeiBanAPI.qrLogin()

    try:
        print('登录成功，userName:' + loginResponse['data']['userName'])
        time.sleep(2)
    except BaseException:
        print('登录失败')
        print(loginResponse)  # TODO: 这里的loginResponse调用没有考虑网络错误等问题
        exit(0)

    # 请求解析并打印用户信息
    try:
        print('请求用户信息')
        stuInfoResponse = WeiBanAPI.getStuInfo(loginResponse['data']['userId'],
                                               tenantCode,
                                               cookie)
        print('用户信息：' + stuInfoResponse['data']['realName'] + '\n'
              + stuInfoResponse['data']['orgName']
              + stuInfoResponse['data']['specialtyName']
              )
        time.sleep(2)
    except BaseException:
        print('解析用户信息失败，将尝试继续运行，请注意运行异常')

    # 请求课程完成进度
    try:
        getProgressResponse = WeiBanAPI.getProgress(loginResponse['data']['preUserProjectId'],
                                                    tenantCode,
                                                    cookie)
        print('课程总数：' + str(getProgressResponse['data']['requiredNum']) + '\n'
              + '完成课程：' +
              str(getProgressResponse['data']['requiredFinishedNum']) + '\n'
              + '结束时间' + str(getProgressResponse['data']['endTime']) + '\n'
              + '剩余天数' + str(getProgressResponse['data']['lastDays'])
              )
        time.sleep(2)
    except BaseException:
        print('解析课程进度失败，将尝试继续运行，请注意运行异常')

    # 请求课程列表
    try:
        getListCategoryResponse = WeiBanAPI.getListCategory(loginResponse['data']['preUserProjectId'],
                                                            '3',
                                                            tenantCode,
                                                            loginResponse['data']['userId'],
                                                            loginResponse['data']['token'])
        time.sleep(2)
    except BaseException:
        print('请求课程列表失败')

    print('解析课程列表并发送完成请求')

    for Category in getListCategoryResponse['data']:
        print('\n----章节码：' + Category['categoryCode'] +
              '章节内容：' + Category['categoryName'])
        try:
            getListCourseResponse = WeiBanAPI.getListCourse(loginResponse['data']['preUserProjectId'],
                                                            '3',
                                                            Category['categoryCode'],
                                                            '',
                                                            loginResponse['data']['userId'],
                                                            tenantCode,
                                                            loginResponse['data']['token'])
            time.sleep(2)
        except BaseException:
            print('请求课程列表失败')
        for j in getListCourseResponse['data']:
            print('课程内容：' + j['resourceName'] +
                  '\nuserCourseId:' + j['userCourseId'])
            if (j['finished'] == 1):
                print('已完成')
            else:
                print('发送完成请求')
                WeiBanAPI.doStudy(
                    loginResponse['data']['preUserProjectId'], j['resourceId'], tenantCode)
                WeiBanAPI.finishCourse(j['userCourseId'], tenantCode, cookie)

                delayInt = WeiBanAPI.getRandomTime()
                print('\n随机延时' + str(delayInt))
                time.sleep(delayInt)


if __name__ == '__main__':
    main()
