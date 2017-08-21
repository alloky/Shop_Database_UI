from gui.locale import rus as locale


class CheckCreator:
    def __init__(self):
        pass

    def write_chck(self, path, order, tm):

        width = 42

        try:
            # if(os.path.exists(path)):
            #     os.rename(path, "{}_old.txt".format(path[:-4]))

            fl = open(path, "w+", encoding="utf-8")

            chck = self.get_template(order, width, tm)

            for line in chck:
                fl.write(line)
                fl.write("\n")

            fl.close()
        except Exception as e:
            raise Exception(e.args[0])

    def get_template(self, order, width, tm):

        _list = []

        _list.append("=" * width)

        _list.append(locale.APP_NAME.center(width, " "))

        _list.append("=" * width)

        _list.append("{} : {}".format(
            locale.CUSTOMER_TITLE,
            order.get_customer().get_full_name()
        ))

        _list.append("{} : {}".format(
            locale.CUSTOMER_SOURCE['phone'],
            order.get_customer().phone))

        _list.append("{} : {}".format(
            locale.CUSTOMER_SOURCE['address'],
            order.get_customer().address))

        _list.append("=" * width)

        for index, item in enumerate(order.get_cart()):
            _list.append("{}. {:.{width}}".format(
                index,
                item.name,
                width=width - 3))
            _list.append("x{:.<{widthL}}{:.>{widthR}}".format(
                item.count,
                item.price * item.count,
                widthL=width // 2,
                widthR=width // 2 + width % 2 - 1))

        _list.append("-" * width)

        _list.append("{:<{widthL}}{:>{widthR}}".format(
            locale.SUM,
            order.get_sum(),
            widthL=width // 2,
            widthR=width // 2 + width % 2))

        _list.append("=" * width)

        _list.append("{} : {}".format(
            locale.DEALS_SOURCE['dttm'],
            tm))

        _list.append("=" * width)

        return _list
