import re
from cpuinfo import get_cpu_info

def map_vendor(vendor):
    """
    Rewrite vendor name
    """
    if vendor == 'GenuineIntel':
        returnval = 'Intel'
    elif vendor == 'AuthenticAMD':
        returnval = 'AMD'
    else:
        returnval = vendor
    return returnval


def clean_cpu_string(brand):
    """
    Rewrite CPU string more neatly.
    
    This:
        Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
    Becomes:
        Intel Core i5-6300U
    """
    # Strip annoying chars
    brand = brand.replace('(R)', '')
    brand = brand.replace('(TM)', '')
    brand = brand.replace('(tm)', '')
    brand = brand.replace('CPU', '')

    # Delete multiple spaces
    re.sub(' +', ' ', brand)

    # Drop the '@ 2.40GHz' suffix
    brand = brand.split('@')[0]

    # Drop the 'with Radeon Graphics' suffix
    brand = brand.split('with')[0]
    brand = brand.strip()

    return brand


def parse_cpu(vendor, cpu):
    """
    Parse the CPU string to figure out some attributes
    """

    cpulabels = {}
    if vendor == 'Intel' and 'Gen' in cpu:
        # 12th Gen Intel(R) Core(TM) i7-1265U
        # 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz
        # 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
        # 11th Gen Intel(R) Core(TM) i7-11700K @ 3.60GHz
        # 11th Gen Intel(R) Core(TM) i9-11900 @ 2.50GHz
        # 12th Gen Intel(R) Core(TM) i3-12100
        # 12th Gen Intel(R) Core(TM) i7-12700
        # 12th Gen Intel(R) Core(TM) i7-12700K
        # 12th Gen Intel(R) Core(TM) i9-12900
        # 12th Gen Intel(R) Core(TM) i9-12900K
        result = re.search(r"(\d{2})th Gen Intel Core (i\d)-(\w+)([A-Z])?", cpu)
        cpulabels['cpuModel'] = result.group(0)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(1)
        cpulabels['cpuLetter'] = result.group(4)

    elif vendor == 'Intel' and 'Xeon' in cpu:
        # Intel(R) Xeon(R) Platinum 8167M CPU @ 2.00GHz
        # Intel(R) Xeon(R) Gold 6226R CPU @ 2.90GHz
        pass

    elif vendor == 'Intel':
        # Intel(R) Core(TM) i5-3470T CPU @ 2.90GHz
        # Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
        # Intel(R) Core(TM) i5-6500T CPU @ 2.50GHz
        # Intel(R) Core(TM) i5-4590T CPU @ 2.00GHz
        # Intel(R) Core(TM) i7-2600 CPU @ 3.40GHz
        # Intel(R) Core(TM) i7-2600S CPU @ 2.80GHz
        # Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz
        # Intel(R) Core(TM) i7-8665U CPU @ 1.90GHz
        result = re.search(r"(i\d)-(\d)?\d{3}([A-Z])?", cpu)
        cpulabels['cpuModel'] = result.group(0)
        cpulabels['cpuFamily'] = result.group(1)
        cpulabels['cpuGeneration'] = result.group(2)
        cpulabels['cpuLetter'] = result.group(3)
    elif vendor == 'AMD' and 'Ryzen' in cpu:
        # AMD Ryzen 7 5700G with Radeon Graphics
        # AMD Ryzen 7 PRO 5850U with Radeon Graphics
        # AMD Ryzen 7 5825U with Radeon Graphics
        # AMD Ryzen 9 5950X 16-Core Processor
        # AMD Ryzen 9 7950X 16-Core Processor
        # AMD Ryzen Threadripper 3990X 64-Core Processor
        result = re.search(r"AMD ((\w+ \d) (\d)\d+([A-Z]?))", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
        cpulabels['cpuLetter'] = result.group(4)
    elif vendor == 'AMD' and 'EPYC' in cpu:
        # AMD EPYC 7J13 64-Core Processor
        # AMD EPYC 7742 64-Core Processor
        # AMD EPYC 7232P 8-Core Processor
        # AMD EPYC 7551P 32-Core Processor
        # AMD EPYC 7642 48-Core Processor
        # AMD EPYC 7F52 16-Core Processor
        # AMD EPYC 7F72 24-Core Processor
        result = re.search(r"AMD ((\w+ \d) (\d)\d+([A-Z]?))", cpu)
        pass
    elif vendor == 'AMD' and 'Opteron' in cpu:
        # AMD Opteron(tm) Processor 4133
        # AMD Opteron(tm) Processor 4310 EE
        # AMD Opteron(tm) Processor 4334
        # AMD Opteron(tm) Processor 6174
        # AMD Opteron(TM) Processor 6238
        # AMD Opteron(tm) Processor 6320
        # AMD Opteron(tm) Processor 6344
        # AMD Opteron(tm) Processor 6366 HE
        # AMD Opteron(tm) Processor 6380
        # Quad-Core AMD Opteron(tm) Processor 2378
        # Quad-Core AMD Opteron(tm) Processor 2384
        # Quad-Core AMD Opteron(tm) Processor 8356
        # Six-Core AMD Opteron(tm) Processor 2427
        # Six-Core AMD Opteron(tm) Processor 8431
        pass
    elif vendor == 'AMD' and 'Athlon' in cpu:
        # AMD Athlon(tm) 5350 APU with Radeon(tm) R3
        pass
    return cpulabels

def drop_nones_inplace(d: dict) -> dict:
    """Recursively drop Nones in dict d in-place and return original dict"""
    dd = drop_nones(d)
    d.clear()
    d.update(dd)
    return d


def drop_nones(d: dict) -> dict:
    """Recursively drop Nones in dict d and return a new dict"""
    dd = {}
    for k, v in d.items():
        if isinstance(v, dict):
            dd[k] = drop_nones(v)
        elif isinstance(v, (list, set, tuple)):
            # note: Nones in lists are not dropped
            # simply add "if vv is not None" at the end if required
            dd[k] = type(v)(drop_nones(vv) if isinstance(vv, dict) else vv
                            for vv in v)
        elif v is not None:
            dd[k] = v
    return dd


def main():
    """main"""
    # Fetch CPU info
    cpuinfo = get_cpu_info()

    # Generate basic labels
    labels = {}
    labels['cpuVendor'] = map_vendor(cpuinfo['vendor_id_raw'])
    labels['cpuString'] = clean_cpu_string(cpuinfo['brand_raw'])

    # Calculate some extra labels
    labels.update(parse_cpu(labels['cpuVendor'], labels['cpuString']))

    # Drop None elements
    labels = (drop_nones_inplace(labels))

    print(labels)

if __name__ == '__main__':
	main()