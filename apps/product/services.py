import os


def delete_files(query=None, file=None):
    if query:
        try:
            for q in query:
                if os.path.isfile(q.photo.path):
                    os.remove(q.photo.path)
        except Exception as e:
            print(e)
        query.delete()

    if file:
        os.remove(file)
