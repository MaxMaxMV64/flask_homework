from tinydb import TinyDB, Query

class Storage:
    def __init__(self, filename="events.json"):
        self.db = TinyDB(filename)
        self.events_table = self.db.table('events')
        self.query = Query()

    def add_event(self, event_date, title, text):
        existing_event = self.events_table.search((self.query.date == event_date))
        if existing_event:
            raise ValueError(f"Событие на дату {event_date} уже существует")
        
        event_data = {"date": event_date, "title": title[:30], "text": text[:200]}
        self.events_table.insert(event_data)
        return event_data

    def list_events(self):
        events = self.events_table.all()
        return events

    def read_event(self, date):
        event = self.events_table.search(self.query.date == date)
        if not event:
            raise ValueError(f"События на дату {date} не найдено")
        return event[0]

    def update_event(self, date, new_title=None, new_text=None):
        event = self.events_table.search(self.query.date == date)
        if not event:
            raise ValueError(f"События на дату {date} не найдено")
        
        event_to_update = event[0]
        if new_title:
            event_to_update["title"] = new_title[:30]
        if new_text:
            event_to_update["text"] = new_text[:200]
        
        self.events_table.update(event_to_update, doc_ids=[event[0].doc_id])
        return event_to_update

    def delete_event(self, date):
        event = self.events_table.remove(self.query.date == date)
        if not event:
            raise ValueError(f"События на дату {date} не найдено")
        return True