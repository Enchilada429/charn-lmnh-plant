"""Script for cleaning and modifying the extracted data."""
from extract import extract_data
import pandas as pd


import pandas as pd


def transform_data(records: list[dict]) -> pd.DataFrame:
    rows = []

    for r in records:

        images = r.get("images") or {}

        rows.append({
            "plant_id": r["plant_id"],
            "plant_name": r["name"],
            "scientific_name": "; ".join(r["scientific_name"]),

            "botanist_name": r["botanist"]["name"],
            "botanist_email": r["botanist"]["email"],
            "botanist_phone": r["botanist"]["phone"],

            "origin_city": r["origin_location"]["city"],
            "origin_country": r["origin_location"]["country"],
            "latitude": r["origin_location"]["latitude"],
            "longitude": r["origin_location"]["longitude"],

            "license": images.get("license"),
            "license_name": images.get("license_name"),
            "license_url": images.get("license_url"),
            "thumbnail": images.get("thumbnail"),

            "last_watered": r["last_watered"],
            "recording_taken": r["recording_taken"],
            "soil_moisture": r["soil_moisture"],
            "temperature": r["temperature"],
        })

    df = pd.DataFrame(rows)

    df["last_watered"] = pd.to_datetime(df["last_watered"], errors="coerce")
    df["recording_taken"] = pd.to_datetime(
        df["recording_taken"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    return df


if __name__ == "__main__":
    data = extract_data()
    df_transformed = transform_data(data)

    print(df_transformed.head(10))
