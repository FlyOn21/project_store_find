from webapp_stores.stores.model import db, Stores, Product
from webapp_stores.user.model import InterestingProduct, User


def save_data(title, online, url, name, icon):
    """
    Функция сохраняет данные о магазине в базу данных Stores
    """
    if Stores.query.filter(Stores.url == url, Stores.name == name).count() \
            and Stores.query.filter(Stores.online != online):
        store = Stores.query.filter(Stores.url == url, Stores.name == name).first()
        store.online = online
        store.title = title
        store.icon = icon
        db.session.add(store)
        db.session.commit()
    else:
        stores = Stores(title=title,
                        online=online,
                        url=url,
                        name=name,
                        icon=icon)
        db.session.add(stores)
        db.session.commit()


def save_data_product(product_dict):
    """
    Функция сохраняет данные о товаре в базу данных Product (все товары)
    """
    if Product.query.filter(Product.id_product == product_dict['id']).count():
        product_b = Product.query.filter(Product.id_product == product_dict['id']).first()
        product_b.prise_full = product_dict['price']
        product_b.prise_discount = product_dict['product_discount']
        product_b.color = product_dict['color']
        product_b.size = str(product_dict['size'])
        product_b.url = product_dict['product_url']
        product_b.image = product_dict['product_image']
        product_b.delivery = (product_dict['delivery'] if 'delivery' in product_dict else None)
        db.session.add(product_b)
        db.session.commit()
    else:
        if product_dict['product_store'] == 'Aliexpress':
            store = 1
        elif product_dict['product_store'] == 'Butik.ru':
            store = 3
        elif product_dict['product_store'] == "Randevu":
            store = 2
        add_product_1 = Product(id_product=product_dict['id'],
                                store=store,
                                name=product_dict['name'],
                                prise_full=product_dict['price'],
                                prise_discount=product_dict['product_discount'],
                                brand=product_dict['brand'],
                                category=product_dict['category'],
                                category_detailed=product_dict['category_detailed'],
                                color=product_dict['color'],
                                size=str(product_dict['size']),
                                url=product_dict['product_url'],
                                image=product_dict['product_image'],
                                delivery=(product_dict['delivery'] if 'delivery' in product_dict else None),
                                other=(product_dict['other'] if 'other' in product_dict else None),
                                gender=product_dict['gender'])
        db.session.add(add_product_1)
        db.session.commit()



def save_interesting_product(product_dict, email=None, price_interesting=None, color_interesting=None,
                             size_interesting=None):
    """
    Функция сохраняет данные о товаре в клиентскую базу данных InterestingProduct
    """
    # Defining user by email (if he has an account, we can connect User and InterestingProduct)
    #print(email)
    try:
        user = User.query.filter(User.email == email).first()
        #print(user)
        id = user.id
        #print(id)
    except:
        id = None

    # Если данный товар уже отслеживается этим клиентом в этом размере (нужно доработать если отслеживается еще по цвету или цене)
    # Нужно добработаь если товара вообще нет в наличие на сайте - словарь может не работать
    if InterestingProduct.query.filter(InterestingProduct.id_store == product_dict['id'],
                                       InterestingProduct.user_email == email,
                                       InterestingProduct.size_interesting == size_interesting).count():
        interesting_product = InterestingProduct.query.filter(InterestingProduct.id_store == product_dict['id'],
                                                              InterestingProduct.user_email == email,
                                                              InterestingProduct.size_interesting == size_interesting).first()
        interesting_product.size_available = str(product_dict['size'])
        interesting_product.price_discount = product_dict['product_discount']
        interesting_product.color = product_dict['color']
        interesting_product.client_id = id if isinstance(id, int) else None

    else:

        interesting_product = InterestingProduct(
            id_store=product_dict['id'],
            store=product_dict['product_store'],
            name=product_dict['name'],

            url=product_dict['product_url'],

            brand=product_dict['brand'],
            category = product_dict['category'],
            category_detailed = product_dict['category_detailed'],
            image = product_dict['product_image'],
            gender = product_dict['gender'],

            prise_full=product_dict['price'],
            prise_discount=product_dict['product_discount'],
            price_interesting=price_interesting,

            size_available=str(product_dict['size']),
            size_possible=str(product_dict['size_possible']) if 'size_possible' in product_dict else None,
            size_interesting=size_interesting,

            color=product_dict['color'],
            color_possible=None,
            color_interesting=color_interesting,

            user_email=email,

            client_id=(id if isinstance(id, int) else None))

    db.session.add(interesting_product)
    db.session.commit()


def create_dict_interesting_products():
    """
    Функция создает словарь типа { id : url } для всех товаров, интересных клиентам
    """
    # Creation of dict = { id : url } for all interesting products
    dict_id_url = {}
    for i in InterestingProduct.query.all():
        dict_id_url[i.id] = i.url
    return dict_id_url


def check_product(info, id):
    """
    Функция проверяет наличие товара, необходимого клиенту, и, в случае наличия, отправляет уведомление клиенту по email
    """
    interesting_product = InterestingProduct.query.filter(InterestingProduct.id == id).first()

    # Updating info about available sizes
    interesting_product.size_available = str(info['size'])
    db.session.add(interesting_product)
    db.session.commit()

    # Informing clients about availability of interesting product
    if interesting_product.size_interesting in interesting_product.size_available:
        if interesting_product.notification_sent==1:
            print(f'Уведомление клиенту {interesting_product.user_email} о товаре уже отправлено {interesting_product.url}')
        else:
            print(
                f'Для клиента {interesting_product.user_email} найден необходимый размер {interesting_product.size_interesting} товара: {interesting_product.url}')
        # Вставить функцию для отправления сообщений на почту + удаление строки ввобще
            interesting_product.notification_sent = 1
            db.session.add(interesting_product)
            db.session.commit()




