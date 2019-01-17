import requests
import re


def getDMproductinfo(txt):
    try:
        EAN = str(re.search('\d{13}', txt).group(0))
    except IndexError:
        print("invalid input")
        return
    url = "https://services.dm.de/product/de/products/gtins/%s?view=details" % EAN
    rPage = requests.get(url)
    productinfo = rPage.json()
    return productinfo


if __name__ == '__main__':
    productinfo = getDMproductinfo("https://www.dm.de/nivea-cellular-elastizitaet-und-kontur-anti-altersflecken-serum-p4005900599407.html")
    productinfo = productinfo[0]
    name = productinfo["name"]
    EAH = productinfo["gtin"]
    brandname = productinfo["brandName"]
    isActive = productinfo["isActive"]
    notDeliverable = productinfo["notDeliverable"]
    notAvailable = productinfo["notAvailable"]
    isNew = productinfo["isNew"]
    isSellout = productinfo["isSellout"]
    isOnlineOnly = productinfo["isOnlineOnly"]
    isDMexclusive = productinfo["isDMExclusive"]
    limitedEdition = productinfo["limitedEdition"]
    notDiscountAllowed = productinfo["notDiscountAllowed"]
    isBranchDeliveryNotPossible = productinfo["isBranchDeliveryNotPossible"]
    nonFoodIngredientStatement = productinfo["nonFoodIngredientStatement"]
    restrictedSpecialOffer = productinfo["restrictedSpecialOffer"]
    purchasable = productinfo["purchasable"]
    price = productinfo["price"]
    netQuantityContent = productinfo["netQuantityContent"]
    contentUnit = productinfo["contentUnit"]
    descriptionText = productinfo["details"]["descriptionText"]
    descriptionRelevantSellingPoints = productinfo["details"]["descriptionRelevantSellingPoints"]
    Ingriedient = productinfo["details"]["descriptionGroup"]["nonFoodIngredientsDescription"]["text"]
#    applicationDescription = productinfo["details"]["descriptionGroup"]["applicationDescription"]["text"]
    print(name, EAH, brandname, isActive, notDeliverable, notAvailable, isNew, isSellout, isOnlineOnly, isDMexclusive, limitedEdition, notDiscountAllowed, isBranchDeliveryNotPossible,
          nonFoodIngredientStatement, restrictedSpecialOffer, purchasable, price, netQuantityContent, contentUnit, descriptionText, descriptionRelevantSellingPoints, Ingriedient)
