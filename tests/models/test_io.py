import embedded_voice_kkutu.models.io as io
import multiprocessing
from time import sleep

def test_io_run_successful():
    # Checks io module not occurs compile error(syntax error) or runtime error
    cio = io.ConcurrencyIO(None, None)
    p = multiprocessing.Process(target=cio.start_io)
    p.start()
    sleep(.5)
    cio.join_io()
    p.terminate()
    sleep(1)
    assert not p.is_alive(), "IO thread should have completed"

def test_fetch_usage():
    cio = io.ConcurrencyIO(None, None)
    q = cio.record_result
    q.append(io.RecordStruct(io.RecordType.stdin_string, 'Test String #1'))
    q.append(io.RecordStruct(io.RecordType.stdin_string, 'Test String #2'))
    q.append(io.RecordStruct(io.RecordType.stdin_string, 'Test String #3'))

    i = 1
    for each in cio.fetch:
        assert each.data == f'Test String #{i}'
        i += 1
