import os

# def dataset_deveice(dev_ratio, test_ratio):
#     folder_num_starts = 2
folder_amount = 2903

ratio = 0.011
data_amount = round(folder_amount*ratio)
gap = folder_amount//data_amount
bias = 2
dev_init = 3 +bias
test_init = gap//2 + bias
dev_folders = ['S' + ("0000" + str(folder_num))[-4:] for folder_num in range(dev_init, folder_amount+bias, gap)]
test_folders = ['S' + ("0000" + str(folder_num))[-4:] for folder_num in range(test_init, folder_amount+bias, gap)]

for item in dev_folders:
    print(item)
print("test")
for item in test_folders:
    print(item)
print(len(dev_folders), len(test_folders), data_amount, gap)