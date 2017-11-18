model_score = 0

l = []

for p in range(1,6000):
    l.append("project-"+str(p))


projects_count = len(l)
for idx, val in enumerate(l):
    if (idx+1) % 500 == 0:
        print("Processing project {0} of {1}".format(idx+1, projects_count))



