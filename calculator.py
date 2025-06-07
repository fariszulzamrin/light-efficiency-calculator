import csv
import os
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class LightData:
    brand: str
    lumens: float
    wattage: float
    hours_per_day: float
    rate_per_kWh: float
    efficacy: Optional[float] = None
    annual_kWh: Optional[float] = None
    annual_cost: Optional[float] = None

def get_float_input(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid input. Please enter a numeric value.")

def get_nonempty_input(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("❌ Input cannot be empty.")

def get_single_light_data(rate_per_kWh: float) -> LightData:
    print("\nEnter details for one light:")
    brand = get_nonempty_input("Brand: ")
    lumens = get_float_input("Lumens: ")
    wattage = get_float_input("Watts: ")
    hours = get_float_input("Usage hours per day: ")

    return LightData(brand=brand, lumens=lumens, wattage=wattage, hours_per_day=hours, rate_per_kWh=rate_per_kWh)

def perform_calculations(data: LightData) -> LightData:
    data.efficacy = data.lumens / data.wattage
    data.annual_kWh = (data.wattage * data.hours_per_day * 365) / 1000
    data.annual_cost = data.annual_kWh * data.rate_per_kWh
    return data

def print_comparison_table(lights: List[LightData]) -> None:
    print("\n📊 Light Comparison Results:")
    print(f"{'Brand':<15}{'Efficacy (lm/W)':<18}{'Annual kWh':<15}{'Annual Cost (€)':<17}")
    print("-"*65)
    for light in lights:
        print(f"{light.brand:<15}{light.efficacy:<18.2f}{light.annual_kWh:<15.2f}{light.annual_cost:<17.2f}")
    # Highlight best efficiency
    best = max(lights, key=lambda x: x.efficacy)
    print(f"\n✅ Most efficient light: {best.brand} with {best.efficacy:.2f} lm/W")

def save_to_csv(lights: List[LightData], file_name="light_results.csv") -> None:
    header = ["Brand", "Lumens", "Watts", "Hours/Day", "Rate €/kWh",
              "Efficacy (lm/W)", "Annual kWh", "Annual Cost (€)"]

    # Read existing data to avoid duplicates
    existing_rows = []
    if os.path.isfile(file_name):
        with open(file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            existing_rows = list(reader)

    def is_duplicate(light: LightData):
        # Check if exact row already exists (excluding header)
        for row in existing_rows[1:]:
            if (row[0] == light.brand and
                float(row[1]) == light.lumens and
                float(row[2]) == light.wattage and
                float(row[3]) == light.hours_per_day and
                float(row[4]) == light.rate_per_kWh):
                return True
        return False

    try:
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            # Write header if file empty or missing header
            if not existing_rows or existing_rows[0] != header:
                writer.writerow(header)
            written = 0
            for light in lights:
                if not is_duplicate(light):
                    writer.writerow([
                        light.brand, light.lumens, light.wattage, light.hours_per_day, light.rate_per_kWh,
                        f"{light.efficacy:.2f}", f"{light.annual_kWh:.2f}", f"{light.annual_cost:.2f}"
                    ])
                    written += 1
            if written > 0:
                print(f"\n📁 {written} new records saved to {file_name}")
            else:
                print("\nℹ️ No new records to save (duplicates detected).")
    except Exception as e:
        print(f"❌ Failed to save to CSV: {e}")

def main() -> None:
    print("💡 Light Efficiency Calculator with Multi-Light Comparison 💡\n")
    rate_per_kWh = get_float_input("Enter electricity cost per kWh (e.g. 0.23 for €0.23): ")

    while True:
        try:
            count = int(input("How many lights do you want to compare? "))
            if count < 1:
                print("❌ Enter a number greater than 0.")
            else:
                break
        except ValueError:
            print("❌ Invalid input. Please enter an integer.")

    lights = []
    for _ in range(count):
        light = get_single_light_data(rate_per_kWh)
        light = perform_calculations(light)
        lights.append(light)

    print_comparison_table(lights)
    save_to_csv(lights)


if __name__ == "__main__":
    main()
