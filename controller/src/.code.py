import gc

print(f"free: {round(gc.mem_free() / 1000, 4)} kB")