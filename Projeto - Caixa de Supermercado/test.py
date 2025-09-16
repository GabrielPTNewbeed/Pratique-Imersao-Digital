#Inserindo Produtos #função 1 # Cashier to input all the products bought one by one #guardamos toda informação no dicionario buyingData
def enterProducts():
    buyingData = {}
    enterDetails = True
    while enterDetails:
        details = input('Press A to product and Q to quit:')
        if details == 'A':
            product = input('Enter product:')
            quantity = int(input('Enter quantity:'))
            buyingData.update({product: quantity})
        elif details =='Q':
            enterDetails = False
        else:
            print('Please select a correct option')
    return buyingData    
#Calculando preço #função 2 # subtotal de um produto, preço, quantidade
def getPrice(product, quantity):
    priceData = {
        'biscuit':3,
        'Chicken':5,
        'Egg':1,
        'Fish':3,
        'Coke':2,
        'Bread':2,
        'Apple':3,
        'Onion':3
    }
    subtotal = priceData[product] * quantity
    print(product + ':$' + str(priceData[product]) +'x'+str(quantity)+'='+str(subtotal))
    return subtotal
#Calculando desconto #função 3 # total da conta e disconto aplicado ou nao
def getDiscount(billAmount, membership):
    discount = 0
    if billAmount >= 25:
        if membership == 'Gold':
            billAmount = billAmount * 0.80
            discount = 20
        elif membership == 'Silver':
            billAmount = billAmount * 0.90
            discount = 10
        elif membership == 'bronze':
            billAmount = billAmount * 0.95
            discount = 5
        print(str(discount) + '% off for'+ membership +''+'membership on total amount: $' + str(billAmount))
    else:
        print('No discount on amount less than $25')
    return billAmount
#Fazendo a conta #função 4 # começo e fim do loop e chama a função 3 para calcular desconto
#parte principal do programa que nao esta dentro de funções, primeira linha do programa a executar começa aqui
def makeBill(buyingData, Membership):
    billAmount = 0
    for key, value in buyingData.items():
        billAmount += getPrice(key, value)
    billAmount = getDiscount(billAmount, Membership)
    print('The discount amount is $' + str(billAmount))
#Texto padrao # faz chamada para função 1 # e faz para a função 4 tambem
buyingData = enterProducts()
membership = input('Enter customer membership:')
makeBill(buyingData, membership)
