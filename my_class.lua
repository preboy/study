-- make class for lua ---
require("utility")

class = 
{
    __call = function(cls, param)
        local o = {}
        setmetatable(o, cls)
        local ctors = {}
        local p = cls
        
        repeat
            if p.ctor ~= nil then
                table.insert(ctors, p.ctor)
            end
            p = getmetatable(p)
        until not p
            
        for i = #ctors, 1, -1 do
            ctors[i](o, param)
        end

        return o
    end,

    extend = function(p, cls)

        cls.__index = cls
        cls.__call = class.__call

        if p then
            setmetatable(cls, p)
        else
            setmetatable(cls, class)
        end

        return cls
    end,

}

Car = class.extend(nil, {
    ctor = function(self, p)
        self.name = p.name
        self.age = p.age
        print_table(p, "Car")
    end,

    run = function(self)
        print("at run : ", self.name, self.age)
    end,} )

c = Car({name = "zcg", age = 23, sex =false})

c:run()

BigCar = class.extend(Car, {
    ctor = function(self, p)
        print_table(p, "BigCar")
    end,

    run = function(self)
        print("BigCar run")
        getmetatable(self).run(self)
    end, })

bc = BigCar({name = "dx", age=  33, sex = true})

bc:run()