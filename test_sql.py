import mysql.connector


def create_connection():
    """创建数据库连接"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="wang",
            password="123",
            database="test"
        )
        print("数据库连接成功")
        return conn
    except mysql.connector.Error as err:
        print(f"连接错误: {err}")
        return None


def create_table(conn):
    """创建数据表"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                age INT
            )
        """)
        print("表创建成功 (如不存在)")
    except mysql.connector.Error as err:
        print(f"创建表错误: {err}")


def insert_data(conn, name, email, age):
    """插入数据"""
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        val = (name, email, age)
        cursor.execute(sql, val)
        conn.commit()
        print(f"插入成功，ID: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print(f"插入错误: {err}")


def query_data(conn):
    """查询数据"""
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        if not results:
            print("没有找到记录")
            return

        print("\n当前用户列表:")
        print("-" * 50)
        for row in results:
            print(f"ID: {row['id']}, 姓名: {row['name']}, 邮箱: {row['email']}, 年龄: {row['age']}")
        print("-" * 50)
        print(f"共找到 {len(results)} 条记录")
    except mysql.connector.Error as err:
        print(f"查询错误: {err}")


def update_data(conn, user_id, new_name, new_age):
    """更新数据"""
    try:
        cursor = conn.cursor()
        sql = "UPDATE users SET name = %s, age = %s WHERE id = %s"
        val = (new_name, new_age, user_id)
        cursor.execute(sql, val)
        conn.commit()
        print(f"更新成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        print(f"更新错误: {err}")


def delete_data(conn, user_id):
    """删除数据"""
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM users WHERE id = %s"
        val = (user_id,)
        cursor.execute(sql, val)
        conn.commit()
        print(f"删除成功，影响行数: {cursor.rowcount}")
    except mysql.connector.Error as err:
        print(f"删除错误: {err}")


def main():
    # 建立连接
    conn = create_connection()
    if not conn:
        return

    try:
        # 创建表
        create_table(conn)

        # 插入示例数据
        print("\n插入测试数据...")
        insert_data(conn, "张三", "zhangsan@example.com", 25)
        insert_data(conn, "李四", "lisi@example.com", 30)

        # 查询数据
        query_data(conn)

        # 更新数据
        print("\n更新张三的信息...")
        update_data(conn, 1, "张三丰", 28)
        query_data(conn)

        # 删除数据
        print("\n删除李四的记录...")
        delete_data(conn, 2)
        query_data(conn)

    finally:
        # 关闭连接
        if conn.is_connected():
            conn.close()
            print("\n数据库连接已关闭")


if __name__ == "__main__":
    main()