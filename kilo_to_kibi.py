import csv

if __name__ == "__main__":
    def kilo_to_kibi(size: str) -> str:
        size = float(size)
        if size >= 1000:
            return str(int(size / 1000 * 1024))
        else:
            return str(int(size))
            
    results_file_name = "./example/results_complete.csv"
    
    with open(results_file_name, "r") as results_file:
        results = list(csv.reader(results_file))
    
    for row in results[1:]:
        row[2] = kilo_to_kibi(row[2])
        row[3] = kilo_to_kibi(row[3])
    
    with open(results_file_name, "w") as results_file:
        writer = csv.writer(results_file)
        writer.writerows(results)
    
    print(results)