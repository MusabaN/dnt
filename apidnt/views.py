from django.shortcuts import render
import requests


def index(request):
    dates = ["2024-03-23",
             "2024-03-24",
             "2024-03-25",
             "2024-03-26",
             "2024-03-27",
             "2024-03-28",
             "2024-03-29",
             "2024-03-30",
             "2024-03-31"
             ]
    # api_url = "https://visbook.dnt.no/api/5702/webproducts/2024-03-27/2024-03-28"

    cottages = {
        "finsehytta": (8591, 137890),
        "kraekkja": (5702, 90637),
        "kjeldebu": (6074, 0)
    }

    finsehytta_availability = all_availabilities(cottages, dates, 0, "finsehytta")
    kjeldebu_availability = all_availabilities(cottages, dates, 1, "kjeldebu")
    kraekkja_availability = all_availabilities(cottages, dates, 2, "kraekkja")

    weekdays = [
        "Lørdag",
        "Søndag",
        "Mandag",
        "Tirsdag",
        "Onsdag",
        "Torsdag"
    ]

    mah_context = zip(weekdays, finsehytta_availability, kjeldebu_availability, kraekkja_availability)

    context = {
        "zipped_lists": mah_context
    }
    return render(request, "apidnt/index.html", context)


def all_availabilities(cottages, dates, start, cottage):
    availabilities = []
    end = 3 - start
    for i in range(start, len(dates) - end):
        accs = get_accomodations(
            cottages[cottage],
            dates[i],
            dates[i + 1]
        )
        availabilities.append(
            get_availability(
                cottages[cottage][1],
                accs
            )
        )

    return availabilities


def get_availability(acc_id, accomodations):
    if acc_id == 0:
        return len(accomodations)
    the_acc = None
    for acc in accomodations:
        if str(acc["id"]) == str(acc_id):
            the_acc = acc
            break
    if the_acc is None:
        return None

    try:
        return int(the_acc["availability"]["steps"][0]["availableUnits"])
    except Exception as e:
        print("Couldnt get available units")
        return None


def get_accomodations(cottage, start_date, end_date):
    api_url = build_api_url(cottage[0], start_date, end_date)
    response = requests.get(api_url)
    res_dict = response.json()
    acc_key = [key for key in res_dict.keys()][0]
    accomodations = res_dict[acc_key]
    return accomodations


def build_api_url(product_id, start_date, end_date):
    return f"https://visbook.dnt.no/api/{product_id}/webproducts/{start_date}/{end_date}"
