import struct

class DataUnpacker():
    def __init__(self, data):
        self._data = data
        self._offset = 0

    def read_uint8(self):
        v = struct.unpack_from("B", self._data, self._offset)
        self._offset += 1
        return v[0]

    def read_uint16(self):
        v = struct.unpack_from("H", self._data, self._offset)
        self._offset += 2
        return v[0]

    def read_uint32(self):
        v = struct.unpack_from("I", self._data, self._offset)
        self._offset += 4
        return v[0]

    def read_uint64(self):
        v = struct.unpack_from("Q", self._data, self._offset)
        self._offset += 8
        return v[0]

    def read_int8(self):
        v = struct.unpack_from("b", self._data, self._offset)
        self._offset += 1
        return v[0]

    def read_int16(self):
        v = struct.unpack_from("h", self._data, self._offset)
        self._offset += 2
        return v[0]

    def read_int32(self):
        v = struct.unpack_from("i", self._data, self._offset)
        self._offset += 4
        return v[0]

    def read_int64(self):
        v = struct.unpack_from("q", self._data, self._offset)
        self._offset += 8
        return v[0]

    #---------------------------------------------------
    def print_offset(self):
        print("offset:", self._offset)

    def skip_bytes(self, n):
        self._offset += n

    def read_bytes(self, n):
        v = struct.unpack_from("{0}b".format(n), self._data, self._offset)
        self._offset += n
        return v

    def read_char(self):
        print(self)
        v = struct.unpack_from("c", self._data, self._offset)
        self._offset += 1
        return v[0]

    def read_string(self):
        text = []
        idx = self._offset
        while True:
            b = self._data[idx]
            if idx == 140:
                pass # print("idx               = ", idx, b, b == '\x00')
            # if b == 0x00:
            if b == '\x00':
                break
            else:
                text.append(b)
                idx += 1
        self._offset += len(text) + 1
        return bytes(text).decode("gbk")

    def read_float(self):
        v = self.read_uint32()
        return float(v)

