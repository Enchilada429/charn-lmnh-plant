"""Script for cleaning and modifying the extracted data."""
from extract import get_all_plants_data
import pandas as pd


def build_dataframe(records: list[dict]) -> pd.DataFrame:
    """Create pandas dataframe from API"""
    rows = []

    for r in records:
        images = r.get("images") or {}

        rows.append({
            "plant_id": r["plant_id"],
            "plant_name": r["name"],
            "scientific_name": "; ".join(r["scientific_name"])
            if "scientific_name" in r and r["scientific_name"]
            else None,

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

    return pd.DataFrame(rows)


def convert_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to correct pandas datatypes"""
    df["last_watered"] = pd.to_datetime(df["last_watered"], errors="coerce")
    df["recording_taken"] = pd.to_datetime(
        df["recording_taken"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["soil_moisture"] = pd.to_numeric(df["soil_moisture"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")

    return df


def drop_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows where soil moisture or temperature is + or - 2 std from mean"""
    sm_mean = df["soil_moisture"].mean()
    sm_std = df["soil_moisture"].std()

    temp_mean = df["temperature"].mean()
    temp_std = df["temperature"].std()

    return df[
        df["soil_moisture"].between(sm_mean - 2 * sm_std, sm_mean + 2 * sm_std) &
        df["temperature"].between(
            temp_mean - 2 * temp_std, temp_mean + 2 * temp_std
        )
    ]


def transform_data(records: list[dict]) -> pd.DataFrame:
    """Calls all transform functions"""
    df = build_dataframe(records)
    df = convert_datatypes(df)
    df = drop_outliers(df)
    return df


if __name__ == "__main__":
    data = get_all_plants_data()
    df_transformed = transform_data(data)

    df_transformed.to_csv("cleaned_data.csv")
