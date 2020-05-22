from scene import *
from scene import *
import random


class MyScene(Scene):
    def setup(self):
        self.setup_object()
        self.reset_game()

    def touch_began(self, touch):
        touch_loc = self.point_from_scene(touch.location)

        if touch_loc in self.button.frame:
            self.button.texture = Texture('pzl:Button2')
            self.reset_game()

            # 役の更新
            self.hand_label.text = self.tg.check_poker_hand()

    def touch_ended(self, touch):
        self.button.texture = Texture('pzl:Button1')

    # カードを画面表示するためのセットアップ
    def set_item(self, id):
        item = self.items[id]
        card = self.tg.draw_cards[id]
        item.texture = Texture('card:' + card['string'])
        item.anchor_point = (0.5, 0)
        # サイズ調整
        self.resize_item(item)

    def setup_object(self):
        # バックグラウンド設定
        self.background_color = '#004f82'
        ground = Node(parent=self)

        # 役の表示
        hand_font = ('Futura', 30)
        self.hand_label = LabelNode('', hand_font, parent=self)
        self.hand_label.position = (self.size.w / 2, self.size.h - 70)
        self.hand_label.z_position = 1

        # ボタン
        self.button = SpriteNode('pzl:Button1', position=(self.size.w / 2, 300))
        self.add_child(self.button)

        button_font = ('Futura', 30)
        self.button_label = LabelNode('Reset', button_font, parent=self, color='black')
        self.button_label.position = (self.size.w / 2, 305)
        self.button_label.z_position = 1

        self.items = []
        self.tg = TrumpGame()
        # カードの初期設定
        for i in range(0, 5):
            item = SpriteNode()
            self.items.append(item)
            item.position = (50 + i * 70, 350)
            self.add_child(item)

    def reset_game(self):
        self.reset_draw_cards()
        # 役の更新
        self.hand_label.text = self.tg.check_poker_hand()

    # カードを5枚引く処理
    def reset_draw_cards(self):
        self.tg.reset_draw_cards(5)
        for i, card in enumerate(self.tg.draw_cards):
            self.set_item(i)

    # サイズ調整
    def resize_item(self, item):
        item.size = (65, 87)


class TrumpGame:
    def make_card_list(self):
        # マークのリスト
        symbol_list = ['Clubs', 'Hearts', 'Spades', 'Diamonds']
        # カードリスト
        card_list = []

        # カードのデータを作成
        for symbol in symbol_list:
            for number in range(1, 14):
                card = {
                    'number': number,
                    'symbol': symbol
                }
                # マークと数字を合体させる
                # 11以上と1は置き換え
                if number == 1:
                    card['string'] = symbol + 'A'
                elif number == 11:
                    card['string'] = symbol + 'J'
                elif number == 12:
                    card['string'] = symbol + 'Q'
                elif number == 13:
                    card['string'] = symbol + 'K'
                else:
                    # 10以下ならそのまま
                    card['string'] = symbol + str(number)

                # カードをリストに追加
                card_list.append(card)

        self.card_list = card_list

    def shuffle(self):
        # カードをシャッフルする
        random.shuffle(self.card_list)

    # 手札を作成する
    def reset_draw_cards(self, number):
        card_list = self.make_card_list()
        self.shuffle()
        self.draw_cards = []

        for i in range(0, number):
            self.draw_cards.append(
                self.card_list.pop(0)
            )

    # 役のチェック処理
    def check_poker_hand(self):
        # ペア数
        pair_count = 0
        # 同じ数字のカウント
        match_count = 0
        # 同じ数字の枚数(3カード,4カードチェック用)
        match_number = 0
        # フラッシュの有無フラグ
        flash_flag = True
        # ストレートの有無フラグ
        straight_flag = True

        # 数字の昇順に並び替える
        cards = sorted(self.draw_cards, key=lambda x: x['number'])

        # チェックループ
        for i in range(1, 5):
            # 前の数字が同じかチェック
            if cards[i]['number'] == cards[i - 1]['number']:
                match_count += 1
                # 最終ループチェック
                if i == 4:
                    if match_count == 1:
                        pair_count += 1
                    # 3カード以上の場合
                    elif match_count > 1:
                        match_number = match_count + 1
            else:
                # 違う数字の場合
                if match_count == 1:
                    pair_count += 1
                # 3カード以上の場合
                elif match_count > 1:
                    match_number = match_count + 1
                match_count = 0
            # 同じマークが続いているかチェック
            if flash_flag == True and cards[i]['symbol'] != cards[i - 1]['symbol']:
                flash_flag = False
            # 数字が連続しているかチェック
            if straight_flag == True and cards[i]['number'] != cards[i - 1]['number'] + 1:
                if cards[i]['number'] != 10 or cards[i - 1]['number'] != 1:
                    straight_flag = False

                # 最終手札チェック
        if straight_flag == True and flash_flag == True:
            if cards[0]['number'] == 1 and cards[4]['number'] == 13:
                # ロイヤルストレートフラッシュ
                hand = 'ロイヤル\nストレートフラッシュ'
            else:
                # ストレートフラッシュ
                hand = 'ストレートフラッシュ'
        elif match_number > 2:
            if match_number == 4:
                # 4カード
                hand = '4カード'
            else:
                if pair_count > 0:
                    # フルハウス
                    hand = 'フルハウス'
                else:
                    # 3カード
                    hand = '3カード'
        elif flash_flag == True:
            # フラッシュ
            hand = 'フラッシュ'
        elif straight_flag == True:
            # ストレート
            hand = 'ストレート'
        elif pair_count > 0:
            if pair_count > 1:
                # 2ペア
                hand = '2ペア'
            else:
                # 1ペア
                hand = '1ペア'
        else:
            # なし
            hand = 'ぶた'

        return hand


if __name__ == '__main__':
    run(MyScene(), show_fps=False)