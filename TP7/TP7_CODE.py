def fusion_tableaux(nums1, nums2):
    i = 0
    j = 0
    resultat = []

    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            resultat.append(nums1[i])
            i += 1
        else:
            resultat.append(nums2[j])
            j += 1

    while i < len(nums1):
        resultat.append(nums1[i])
        i += 1

    while j < len(nums2):
        resultat.append(nums2[j])
        j += 1

    return resultat


entree1 = input("Entrez les éléments triés de nums1 séparés par des espaces : ")
entree2 = input("Entrez les éléments triés de nums2 séparés par des espaces : ")

nums1 = list(map(int, entree1.split()))
nums2 = list(map(int, entree2.split()))

resultat = fusion_tableaux(nums1, nums2)

print("Tableau fusionné :", resultat)