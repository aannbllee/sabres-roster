import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup


URL = "https://www.nhl.com/sabres/roster"
OUTPUT_CSV = Path(__file__).with_name("sabres_roster.csv")


def fetch_player_rows(url: str = URL) -> list[dict[str, str]]:
	response = requests.get(
		url,
		headers={
			"User-Agent": (
				"Mozilla/5.0 (X11; Linux x86_64) "
				"AppleWebKit/537.36 (KHTML, like Gecko) "
				"Chrome/124.0.0.0 Safari/537.36"
			)
		},
		timeout=30,
	)
	response.raise_for_status()

	soup = BeautifulSoup(response.text, "html.parser")

	rows: list[dict[str, str]] = []

	# NHL roster tables typically use table rows
	player_rows = soup.find_all("tr")

	for row in player_rows:
		columns = row.find_all("td")

		# Skip non-player rows
		if len(columns) < 6:
			continue

		try:
			jersey_number = columns[0].get_text(strip=True)
			player_name = columns[1].get_text(strip=True)
			position = columns[2].get_text(strip=True)
			shoots = columns[3].get_text(strip=True)
			height = columns[4].get_text(strip=True)
			weight = columns[5].get_text(strip=True)

			rows.append(
				{
					"player_name": player_name,
					"jersey_number": jersey_number,
					"position": position,
					"shoots": shoots,
					"height": height,
					"weight": weight,
				}
			)

		except Exception:
			continue

	rows.sort(key=lambda row: row["player_name"])
	return rows


def write_csv(rows: list[dict[str, str]], output_path: Path = OUTPUT_CSV) -> None:
	output_path.parent.mkdir(parents=True, exist_ok=True)

	with output_path.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.DictWriter(
			csv_file,
			fieldnames=[
				"player_name",
				"jersey_number",
				"position",
				"shoots",
				"height",
				"weight",
			],
		)

		writer.writeheader()
		writer.writerows(rows)


def main() -> None:
	rows = fetch_player_rows()
	write_csv(rows)
	print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
	main()