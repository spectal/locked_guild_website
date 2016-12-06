import os
import tornado.ioloop
import tornado.template as template
import tornado.web
from wow_api_modules import Guild_Members


class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "guild_members/css/"),
            "pictures_path": os.path.join(os.path.dirname(__file__), "guild_members/class_icons/")
        }
        handlers = [
            (r'/guild_members/', GuildMemberSite),
            (r'/css/(main\.css)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
            (r'/class_icons/(.*)', tornado.web.StaticFileHandler, dict(path=settings['pictures_path'])),

        ]
        tornado.web.Application.__init__(self, handlers, **settings)
        print self.settings

class GuildMemberSite(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "text/html")
        self.write(self.build_page())

    def build_page(self):
        loader = template.Loader("guild_members/templates/")
        guild_member_page = loader.load("character_attribs.html").generate(members=self.build_member_info())
        return guild_member_page

    @staticmethod
    def build_member_info():
        get_member_data = Guild_Members.GuildMember('all')
        members = get_member_data.return_guild_member_data()
        member_list = {}
        for key in members.iterkeys():
            member_attribs = []
            for index, item in enumerate(members.get(key)):
                member = []
                if str(item) != str(key):
                    member_attribs.append(item + ' ')
                    member.append(member_attribs)
                if index == len(members.get(key)) - 1:
                    member_list[key] = member
        return member_list


class SingleMemberSite(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "text/html")
        self.write(self.build_page())

    def build_page(self):
        loader = template.Loader("guild_members/templates/")
        single_member_page = loader.load("single_character_page.html").generate()
        return single_member_page


def make_app():
    return Application()


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
