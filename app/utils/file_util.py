# 文件处理（附件上传、PDF导出、Excel导入导出）
# 文件处理（附件上传、PDF导出、Excel导入导出）
import pandas as pd
from io import BytesIO


def export_to_excel(data: list, sheet_name: str) -> BytesIO:
    """
    将数据导出为Excel格式
    :param data: 要导出的数据列表
    :param sheet_name: Excel工作表名称
    :return: BytesIO对象
    """
    df = pd.DataFrame(data)
    
    # 创建一个 BytesIO 对象
    output = BytesIO()
    
    # 使用 pandas 的 to_excel 方法将数据写入 BytesIO
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # 移动文件指针到开始位置
    output.seek(0)
    
    return output
