



-- ZeroTable
-------------------------------------------

-- 为表设置一些默认值
DefaultValue = function(t, val)
    assert(val, "val must be present.")
    local _mtable =
    {
        __index = function(t, n)
            rawset(t, n, val)
            return val
        end,
    }
    setmetatable(t, _mtable)
end


-- 将表未赋值的项设置为0
ZeroTable = function(t)
    DefaultValue(t, 0)
end

local ttt = {}
DefaultValue(ttt, {"i come", "i fuck", "i phone", })

zcg_print(ttt.str)
zcg_print(ttt[223])



-- 计算宝宝100天的mysql方法
select DATE_ADD('2014-04-07',interval 100 day)
