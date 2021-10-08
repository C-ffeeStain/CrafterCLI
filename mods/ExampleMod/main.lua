local mod = {}

mod.meta = {
    name = "ExampleMod",
    version = "1.0",
    description = "An example mod.",
    author = "Example Author",
}

function main()
    print("Example mod loaded!")
    add_material("example_material")
    add_item("example", {"example_material", "water"})
end
