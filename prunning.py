import copy
from random import randint
import dec_tree_func as dt

# file_name = "lenses/lenses.txt"
file_name = "car/car.txt"
train_vectors, train_classes, test_vectors, test_classes = dt.load_data_odd_even(file_name)
num_of_train_examples = train_classes.__len__()
num_of_test_examples = test_classes.__len__()

def preorder (temptree, number):
    if isinstance(temptree, dict):
        attribute = list(temptree.keys())[0]
        if temptree[attribute]['number'] == number:
            if(temptree[attribute][0]!=0 and temptree[attribute][0]!=1):
                temp_tree = temptree[attribute][0]
                if isinstance(temp_tree, dict):
                    temp_attribute = list(temp_tree.keys())[0]
                    temptree[attribute][0] = temp_tree[temp_attribute]['best_class']
            elif(temptree[attribute][1]!=0 and temptree[attribute][1]!=1):
                temp_tree = temptree[attribute][1]
                if isinstance(temp_tree, dict):
                    temp_attribute = list(temp_tree.keys())[0]
                    temptree[attribute][1] = temp_tree[temp_attribute]['best_class']
        else:
            left = temptree[attribute][0]
            right = temptree[attribute][1]
            preorder(left, number)
            preorder(right,number )
    return temptree

def count_number_of_non_leaf_nodes(tree):
    if isinstance(tree, dict):
        attribute = list(tree.keys())[0]
        left = tree[attribute][0]
        right = tree[attribute][1]
        return (1 + count_number_of_non_leaf_nodes(left) +
               count_number_of_non_leaf_nodes(right));
    else:
        return 0;

def post_prune(L, K, tree):
    best_tree = tree
    for i in range(1, L+1) :
        temp_tree = copy.deepcopy(best_tree)
        M = randint(1, K);
        for j in range(1, M+1):
            n = count_number_of_non_leaf_nodes(temp_tree)
            if n> 0:
                P = randint(1,n)
            else:
                P = 0
            preorder(temp_tree, P)
        num_of_training_errorsB = dt.calc_error(train_vectors, train_classes, best_tree)
        accuracyBeforePruning = str(num_of_training_errorsB/num_of_train_examples)
        num_of_test_errorsB = dt.calc_error(test_vectors, test_classes, tree)
        accuracyBeforePruning += str(num_of_test_errorsB / num_of_test_examples)
        num_of_training_errors = dt.calc_error(train_vectors, train_classes, temp_tree)
        accuracy_after_pruning = str(num_of_training_errors/num_of_train_examples)
        num_of_test_errors = dt.calc_error(test_vectors, test_classes, tree)
        accuracy_after_pruning += str(num_of_test_errors/num_of_test_examples)
        if accuracy_after_pruning >= accuracyBeforePruning:
            best_tree = temp_tree
    return best_tree

def pruneLeaves(obj):
    """takes decision tree as parameter and returns a pruned tree based on chi square
    params:
        obj (dict):
        obj is a decision tree encoded in the form of decision tree
    return:
         obj (dict):
         obj is decision tree with pruned leaves
    """
    isLeaf = True
    parent = None
    for key in obj:
        if isinstance(obj[key], dict):
            isLeaf = False
            parent = key
            break
    if isLeaf and obj.keys()[0].split(' ')[0] not in satisfied_attributes:
        global pruned
        pruned = True
        return 'pruned'
    if not isLeaf:
        if pruneLeaves(obj[parent]):
            obj[parent] = None
    return obj

def prune(tree):
    pruned = True
    while pruned:
        # keep pruning till leaf nodes can be pruned or till whole tree has been pruned
        pruned = False
        tree = pruneLeaves(tree)
        if tree == 'pruned':
            break
    return tree

def accurateRate(myTree,dataSet,labels):
   # import pickle
   # fr=open('tree_1.txt')
   # myTree=pickle.load(fr)
    count=[]
    for testVec in dataSet:
        temp=classify(myTree,labels,testVec,count)
 #   print count
    accurateRate=float(len(count))/len(dataSet)
    percentage=accurateRate*100
    output=str(percentage)
    #print 'The accuracy is '+output+'%'
    return percentage

def get_pathes(the_model):
    pathes = []
    def prune_model(model, path):
        if (type(model) is dict):
            for key in model.keys():
                path.append(key)
                prune_model(model[key], copy.deepcopy(path))
                path.remove(key)
        else:
            path.pop(len(path)-1)
            pathes.append(path)
            return
    prune_model(the_model, [])
    return pathes

def prune1(myTree,dataSet,labels):
    bestpercentage=76.12
    pathes=get_pathes(myTree)
    unique_box=unique_pathes(pathes)
    percentage_1=0
    percentage_2=0
    for path in unique_box:
        #print path
        #print (accurateRate(myTree,dataSet,labels))
        Zero=copy.deepcopy(myTree)
        replace_subtree_0(Zero,path)
        percentage_1=accurateRate(Zero,dataSet,labels)
       # print percentage_1
        One=copy.deepcopy(myTree)
        replace_subtree_1(One,path)
        percentage_2=accurateRate(One,dataSet,labels)
       # print percentage_2
        if percentage_1>percentage_2 and percentage_1>bestpercentage:
            bestpercentage=percentage_1
            bestTree=Zero
        if percentage_2>percentage_1 and percentage_2>bestpercentage:
            bestpercentage=percentage_2
            bestTree=One
    return bestTree

# # Count leaves in a tree
# def countLeaves(decisiontree):
#     if decisiontree.isLeaf:
#         return 1
#     else:
#         n = 0
#         for child in decisiontree.children:
#             n += countLeaves(child)
#     return n
#
#
# # Check if a node is a twig
# def isTwig(decisionTree):
#     for child in decisiontree.children:
#         if not child.isLeaf:
#             return False
#     return True
#
#
# # Make a heap of twigs.  The default heap is empty
# def collectTwigs(decisionTree, heap=[]):
#     if isTwig(decisionTree):
#         heappush(heap,(decisionTree.@nodeInformationGain, decisionTree))
#     else:
#         for child in decisiontree.children:
#             collectTwigs(child,heap)
#     return heap
#
#
# # Prune a tree to have nLeaves leaves
# # Assuming heappop pops smallest value
# def prune(dTree, nLeaves):
#     totalLeaves = countLeaves(dTtree)
#     twigHeap = collectTwigs(dTree)
#     while totalLeaves > nLeaves:
#         twig = heappop(twigHeap)
#         totalLeaves -= (length(twig.@children) - 1) #Trimming the twig removes
#                                                     #numChildren leaves, but adds
#                                                     #the twig itself as a leaf
#         twig.@chidren = null  # Kill the chilren
#         twig.@isLeaf = True
#         twig.@nodeInformationGain = 0
#
#         # Check if the parent is a twig and, if so, put it in the heap
#         parent = twig.@parent
#         if isTwig(parent):
#             heappush(twigHeap,(parent.@nodeInformationGain, parent))
#     return