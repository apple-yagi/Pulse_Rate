import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Pulse_Rate


class Command(BaseCommand):
    help = "Backup Pulse_Rate data"

    def handle(self, *args, **options):
        # 実行時のYYYYMMDDを取得
        date = datetime.date.today().strftime("%Y%m%d")

        # 保存ファイルの相対パス
        file_path = settings.BACKUP_PATH + 'pulse_rate_' + date + '.csv'

        # 保存ディレクトリが存在しなければ作成
        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        # バックアップファイルの作成
        with open(file_path, 'w')as file:
            writer = csv.writer(file)

            # ヘッダーの書き込み
            header = [field.name for field in Pulse_Rate._meta.fields]
            writer.writerow(header)

            # Pulse_Rateテーブルの全データを取得
            pulse_rates = Pulse_Rate.objects.all()

            for pulse_rate in pulse_rates:
                writer.writerow([str(pulse_rate.user),
                                 pulse_rate.title,
                                 str(pulse_rate.data),
                                 str(pulse_rate.created_at),
                                 str(pulse_rate.updated_at)])

            # 保存ディレクトリのファイルリストを取得
            files = os.listdir(settings.BACKUP_PATH)
            # ファイルが設定以上あったら一番古いファイルを削除
            if len(files) >= settings.NUM_SAVED_BACKUP:
                files.sort()
                os.remove(settings.BACKUP_PATH + files[0])