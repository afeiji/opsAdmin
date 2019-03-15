#encoding:utf-8

from rest_framework import serializers
from .models import Publish, Book,Author


class PublishSerializer(serializers.ModelSerializer):

    class Meta():
        model = Publish
        # fields表示要序列化哪些字段
        # fields = ("id", "name", "city", "address")
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        instance = self.Meta.model.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        print(validated_data)
        self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
        return instance

# class BookSerializer(serializers.ModelSerializer):
#
#     class Meta():
#         model = Book
#         # fields表示要序列化哪些字段
#         fields = ("id", "name", "authors", "publisher","publication_date")


class BookSerializer(serializers.ModelSerializer):
    # publisher = PublishSerializer()         # 一对多，默认显示PublishSerializer定义的所有列
    # authors = AuthorSerializer(many=True)   # 多对多，默认显示AuthorSerializer所有的列
    # publication_date = serializers.DateTimeField(format="%Y-%m-%d")   ＃ 后端格式化序列化输出的时间

    class Meta:
        model = Book
        fields = "__all__"

    def author(self, author_queryset):
        print("author_queryset:",author_queryset)
        ret = []
        # 多对多的结果是一个列表对象，需要遍历对象，将需要序列化的内容提出来即可
        for author in author_queryset:
            ret.append({
                'id': author.id,
                'name': author.name,
                'email': author.email
            })
        return ret

    # 重写to_representation方法，定义关系表中要序列化输出的列，默认只输出关系表对应列的ID
    def to_representation(self, instance):
        # 一对多关系，相当于一对多的正向查询。获取当前书的出版商，SQL：Book.objects.get(pk=1).publisher
        publisher_obj = instance.publisher
        # 多对多，相当于多对多的正向查询。获取当前书的作者，SQL：Book.objects.get(pk=1).authors.all()
        authors_obj = self.author(instance.authors.all())
        # print(instance)
        # print(publisher_obj)
        # print(authors_obj)

        # 将书的相关信息序列化，即将Book.objects.all()的querydict结果集合转为JSON
        ret = super(BookSerializer, self).to_representation(instance)

        # 将关联表需要序列化输出的列处理为json,也加入序列化大字典中。这样就能序列化出当前表和关联表所有想展示的字段了
        ret["publisher"] = {
            "id": publisher_obj.id,
            "name": publisher_obj.name,
            "address": publisher_obj.address
        },
        ret["authors"] = authors_obj
        #print(ret)
        return ret

    # def to_internal_value(self, data):
    #     print(data)

    # 重写create方法，源码中已经对单表、一对多、多对多对关系做了处理，此次为了学习调试方便重写
    def create(self, validated_data):
        # {'name': '平凡的世界', 'publication_date': datetime.date(2018, 5, 10),
        # 'publisher': <Publish: Publish object>, 'authors': [<Author: Author object>]}
        print(validated_data)
        author_list = validated_data.pop('authors', [])
        instance = self.Meta.model.objects.create(**validated_data)
        # author和book是多对多关系，添加数据时需要单独处理
        instance.authors.add(*author_list)
        return instance

    # 源码中已经对单表、一对多、多对多对关系做了处理，此次为了学习调试方便重写
    def update(self, instance, validated_data):
        print(validated_data)
        author_list = validated_data.pop('authors', [])
        self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
        # 多对多添加的两种写法
        instance.authors.set(author_list)
        return instance

class AuthorSerializer(serializers.ModelSerializer):

    class Meta():
        model = Author
        # fields表示要序列化哪些字段
        fields = ("id", "name", "email", "phone","address")