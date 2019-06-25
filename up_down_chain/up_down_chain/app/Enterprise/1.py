import pymysql

import random
import time

def mysql():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", db="UpdownChain_alpha", charset="utf8",
                           passwd="mysql")
    cursor = conn.cursor()

    sql1 = "select company_id from s_ggsh"
    cursor.execute(sql1)
    res1 = cursor.fetchall()

    try:

        dict_data = {"a_nlmy":"A_count", "b_cky":"B_count", "c_zzy":"C_count", "d_drrsgy":"D_count", "e_jzy":"E_count", "f_pflsy":"F_count", "g_jcy":"G_count", "h_zscyy":"H_count", "i_xxrjy":"I_count", "j_jry":"J_count",
                     "k_fdcy":"K_count", "l_zlsw":"L_count", "m_kyjs":"M_count", "n_slhjgg":"N_count", "o_jmxl":"O_count", "p_jy":"P_count", "q_wssh":"Q_count", "r_wty":"R_count", "s_ggsh":"S_count", "t_gj":"T_count"}

        # res1.count()





        for i in res1:
            num1 = random.randint(500, 1000)
            num2 = random.randint(1, 200)

            sql = "update  S_count set access_count=%d,recommended_count=%d WHERE company_id='%s'" % (
            num1, num2, i[0])
            cursor.execute(sql)
            conn.commit()


    except:
        print("查询出错")

    cursor.close()

    conn.close()

time_start = time.time()
mysql()
time_end = time.time()
print(time_end-time_start)
