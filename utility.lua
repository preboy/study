
--[[

    Ŀ�ģ��ṩһЩ���õĺ���


   ------ export functions -----

    ��ӡ����t������,���name���ڣ����ȴ�ӡ��name
    zcg_print(t, name):



]]

-- ��ӡǰ׺
local function _print_prefix(str, n)
    for i = 1, n, 1 do
        io.write("    ")
    end
    io.write(str)
end


-- ��ӡ��
local function _print_table(t, depth)
    _print_prefix("{\n", depth)
    for k, v in pairs(t) do
        _print_prefix(k .. " = ", depth + 1)
        if type(v) == "number" then
            io.write(v .. ",\n")
        elseif type(v) == "string" then
            io.write("\"" .. v .. "\",\n")
        elseif type(v) == "table" then
            io.write("\n")
            _print_table(v, depth + 1)
        elseif type(v) == "boolean" then
            io.write(tostring(v) .. ",\n")
        else
            io.write("type \'" .. type(v) .. "\' not supported print.\n")
        end
    end
    _print_prefix("},", depth)
    io.write("\n")
end


-- print table to console
zcg_print = function(t, table_name, file_path)
    if file_path then
        local f = io.open(file_path, "w+")
        io.output(f)
    end

    if type(t) ~= "table" then
        if table_name then
            io.write(string.format("%s = ", table_name))
        end
        io.write(t, "\n")
        return
    end

    if table_name then
        io.write(table_name .. " = \n")
    end

    depth = 0
    _print_table(t, depth)

    if file_path then
        local f = io.output(io.stdout)
        io.close(f)
    end
end


-- ��ȡ��Ĵ�С
zcg_TableSize = function(t)
    local count = 0
    for k, v in pairs(t) do
        count  = count + 1
    end
    return count
end


-- ��¼��־���ļ�
zcg_log = function(fname, str)
    local p = io.open(fname, "a+")
    p:write(str)
    io.close(p)
end



----- add to system lib -----------------------------------------------------------

string.split = function (str, sep)
    sep = sep or " "

    local t = {}
    for v in string.gmatch(str, "[^"..sep.."]+") do
        table.insert(t, v)
    end
    return t
end
