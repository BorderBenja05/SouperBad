def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip().split() for line in lines]

def write_file(file_path, data):
    with open(file_path, 'w') as file:
        for name, number in data:
            file.write(f"{name} {number}\n")

def sort_data(data):
    return sorted(data, key=lambda x: int(x[1]), reverse=True)

def main(input_file, output_file):
    data = read_file(input_file)
    sorted_data = sort_data(data)
    write_file(output_file, sorted_data)

if __name__ == "__main__":
    input_file = 'data_hogs.txt'  # Replace with your input file path
    output_file = 'output.txt'  # Replace with your output file path
    main(input_file, output_file)