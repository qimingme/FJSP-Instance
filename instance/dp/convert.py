import os


def convert_fjs_format(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # 解析第一行
    first_line = lines[0].split()
    num_jobs = int(first_line[0])
    num_machines = int(first_line[1])

    # 计算最大候选机器数C
    max_c = 0
    job_data = []

    for job_idx in range(num_jobs):
        parts = list(map(int, lines[job_idx + 1].split()))
        idx = 0
        num_operations = parts[idx]
        idx += 1
        operations = []

        for _ in range(num_operations):
            num_options = parts[idx]
            max_c = max(max_c, num_options)
            idx += 1
            options = []

            for __ in range(num_options):
                # 机器编号从0开始（原编号-1）
                machine = parts[idx] - 1
                duration = parts[idx + 1]
                options.append((machine, duration))
                idx += 2

            operations.append((num_options, options))

        job_data.append((num_operations, operations))

    # 写入新格式
    with open(output_file, 'w') as f:
        # 写入第一行
        f.write(f"{num_jobs} {num_machines} {max_c}\n")

        # 写入每个任务（任务编号隐式从0开始）
        for job in job_data:
            num_operations, operations = job
            line_parts = [str(num_operations)]

            for op in operations:
                num_options, options = op
                op_parts = [str(num_options)]

                for machine, duration in options:
                    op_parts.append(f"{machine} {duration}")

                line_parts.append(" ".join(op_parts))

            # 使用4个空格作为分隔符
            f.write("    ".join(line_parts) + "\n")


def batch_convert_files():
    # 创建输出目录
    os.makedirs("converted", exist_ok=True)

    # 处理1a到18a文件
    for i in range(1, 19):
        input_filename = f"DPpaulli{i}a.fjs"
        output_filename = os.path.join("converted", f"DPpaulli{i}a_converted.txt")

        if os.path.exists(input_filename):
            try:
                convert_fjs_format(input_filename, output_filename)
                print(f"成功转换: {input_filename} -> {output_filename}")
            except Exception as e:
                print(f"转换失败 {input_filename}: {str(e)}")
        else:
            print(f"文件不存在: {input_filename}")


if __name__ == "__main__":
    batch_convert_files()
