import csv
import os
import time

def filter_csv(input_file, columns_to_keep, row_filter=None, separator=","):
    output_file = os.path.join(
        os.path.dirname(input_file),
        "filtered_" + os.path.basename(input_file)
    )

    row_count = 0
    kept_rows = 0
    with open(input_file, mode="r", encoding="ISO-8859-1", newline="") as infile:
        reader = csv.DictReader(infile, delimiter=separator)
        filtered_fieldnames = [col for col in reader.fieldnames if col in columns_to_keep]

        with open(output_file, mode="w", encoding="ISO-8859-1", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=filtered_fieldnames)
            writer.writeheader()
            for row in reader:
                row_count += 1
                # Apply row filter if provided
                if row_filter:
                    col, value, include = row_filter
                    if include and row[col] != value:
                        continue
                    if not include and row[col] == value:
                        continue
                writer.writerow({col: row[col] for col in filtered_fieldnames})
                kept_rows += 1

    return output_file, len(columns_to_keep), row_count, kept_rows, len(reader.fieldnames)


def format_size(bytes_val):
    """Convert bytes into human-readable KB/MB/GB string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} TB"


def main():
    input_file = input("Enter path to CSV file: ").strip()
    if not os.path.isfile(input_file):
        print("❌ File not found.")
        return

    input_size = os.path.getsize(input_file)

    sep_input = input("Enter separator (press Enter for comma): ").strip()
    separator = sep_input if sep_input else ","
    if separator == "\\t":
        separator = "\t"

    with open(input_file, mode="r", encoding="ISO-8859-1", newline="") as infile:
        reader = csv.DictReader(infile, delimiter=separator)
        all_columns = reader.fieldnames

    if not all_columns:
        print("❌ No columns found in the CSV.")
        return

    print("\nAvailable columns:")
    for i, col in enumerate(all_columns):
        print(f"{i}: {col}")

    default_indices = [1, 11, 12, 14, 16, 27, 30, 31]
    default_valid = [i for i in default_indices if i < len(all_columns)]
    default_names = [all_columns[i] for i in default_valid]
    default_str = ",".join(str(i) for i in default_valid)
    print(f"\nDefault suggestion: {default_str}")
    for i, name in zip(default_valid, default_names):
        print(f"  {i}: {name}")

    cols_input = input(
        f"\nEnter column numbers or names to keep (comma-separated) [default: {default_str}]: "
    ).strip()
    if not cols_input:
        cols_input = default_str

    selected_columns = []
    for item in cols_input.split(","):
        item = item.strip()
        if not item:
            continue
        if item.isdigit():  # index
            idx = int(item)
            if 0 <= idx < len(all_columns):
                selected_columns.append(all_columns[idx])
            else:
                print(f"⚠️ Index {idx} is out of range, ignored.")
        else:  # name
            if item in all_columns:
                selected_columns.append(item)
            else:
                print(f"⚠️ Column name '{item}' not found, ignored.")

    if not selected_columns:
        print("⚠️ No valid columns selected.")
        return

    # Remove duplicates while preserving order
    seen = set()
    selected_columns = [c for c in selected_columns if not (c in seen or seen.add(c))]

    # Optional row filter
    row_filter = None
    use_filter = input("\nDo you want to filter rows based on a column value? (y/n): ").strip().lower()
    if use_filter == "y":
        filter_col = input("Enter column name to filter on: ").strip()
        if filter_col not in all_columns:
            print(f"❌ Column '{filter_col}' not found.")
            return

        # Collect unique values from that column
        unique_values = set()
        with open(input_file, mode="r", encoding="ISO-8859-1", newline="") as infile:
            reader = csv.DictReader(infile, delimiter=separator)
            for row in reader:
                unique_values.add(row[filter_col])

        print(f"\nUnique values in column '{filter_col}':")
        for val in sorted(unique_values):
            print(f"  - {val}")

        filter_val = input("\nEnter value to filter by: ").strip()
        if filter_val not in unique_values:
            print(f"⚠️ Warning: '{filter_val}' was not found in column '{filter_col}'.")
        include = input("Keep rows with this value? (y/n): ").strip().lower() == "y"
        row_filter = (filter_col, filter_val, include)

    # Process
    start_time = time.time()
    output_file, kept_cols, total_rows, kept_rows, total_cols = filter_csv(
        input_file, selected_columns, row_filter, separator
    )
    elapsed = time.time() - start_time
    output_size = os.path.getsize(output_file)

    # Calculate percentage reduction
    reduction_pct = 0.0
    if input_size > 0:
        reduction_pct = (1 - (output_size / input_size)) * 100

    # ✅ Print metrics
    print("\n=== Process Summary ===")
    print(f"Input file     : {input_file}")
    print(f"Output file    : {output_file}")
    print(f"Input size     : {format_size(input_size)}")
    print(f"Output size    : {format_size(output_size)}")
    print(f"Size reduction : {reduction_pct:.2f}%")
    print(f"Total columns  : {total_cols}")
    print(f"Columns kept   : {kept_cols} → {selected_columns}")
    print(f"Rows processed : {total_rows}")
    print(f"Rows kept      : {kept_rows}")
    print(f"Elapsed time   : {elapsed:.2f} seconds")
    print("========================\n")


if __name__ == "__main__":
    main()
