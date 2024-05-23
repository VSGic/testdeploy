import csv

def parse_results():
    with open("./locust_output_stats.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Name'] == 'Aggregated':
                print("Summary of Load Test:")
                print(f"Total Requests: {row['Requests']}")
                print(f"Failures: {row['Failures']}")
                print(f"Average Response Time: {row['Average Response Time']} ms")
                print(f"95th Percentile Response Time: {row['95%']} ms")
                print(f"Average Content Size: {row['Average Content Size']} bytes")
                print(f"Requests per Second: {row['Requests/s']}")
                print(f"Failure Ratio: {row['Failure Rate']}")
                break

if __name__ == "__main__":
    parse_results()
