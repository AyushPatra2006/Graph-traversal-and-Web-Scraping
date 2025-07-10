'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 4 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP4
Student 1: Ayush Patra, apatra8
Student 2: <Name>, <NETID>
Student 3: <Name>, <NETID>
Student 4: <Name>, <NETID>
'''
from collections import deque
import pandas as pd
from selenium.webdriver.common.by import By
from io import StringIO
import time
import requests
class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ 
        Leave this method as is! It will be over-written the child classes
        Each child class should perform the following:
            Record the node value in self.order AND return its children
            parameter: node
            return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set and order list
        self.visited.clear()
        self.order.clear()
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)
    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. call self.visit_and_get_children(node) to get the children
        children = self.visit_and_get_children(node)
        # 4. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
    def bfs_search(self,node):
        self.visited.clear()
        self.order.clear()
        self.bfs_visit(node) 
    def bfs_visit(self, node):
        queue = deque([node])
        self.visited.add(node)

        while queue:
            current = queue.popleft()
            children = self.visit_and_get_children(current)
            for child in children:
                if child not in self.visited:
                    self.visited.add(child)
                    queue.append(child)
            
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        self.order.append(node)
        children = []
        for child, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(child)
        # TODO: use `self.df` to determine what children the node has and append them
        return children
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
    def visit_and_get_children(self, node):
        with open(f"file_nodes/{node}", 'r') as f:
            lines = f.read().splitlines()
            value = lines[0]
            children_line = lines[1] if len(lines) > 1 else ""
            children = [child.strip() for child in children_line.split(",") if child.strip()]

        self.order.append(value)
        return children
    def concat_order(self):
        return ''.join(self.order)
class WebSearcher(GraphSearcher):
    def __init__(self,driver):
        super().__init__()
        self.driver = driver
        self.tables = []
    def visit_and_get_children(self, node):
        self.order.append(node)
        self.driver.get(node)
        links = []
        for elem in self.driver.find_elements("tag name", "a"):
            href = elem.get_attribute("href")
            if href:
                links.append(href)
        try:
            page_tables = pd.read_html(StringIO(self.driver.page_source))[0]
            self.tables.append(page_tables)  # accumulate tables
        except ValueError:
            # pandas raises ValueError if no tables are found
            pass
        return links
    def table(self):
        wanted_tables = self.tables
        # concatenate them into one big DataFrame
        if wanted_tables:
            df = pd.concat(wanted_tables, ignore_index=True)
            df = df.dropna(axis=1, how='all')
            return df
        else:
            return pd.DataFrame() 
def reveal_secrets(driver, url, travellog):
    password = ''.join(str(int(clue)) for clue in travellog["clue"])
    driver.get(url)
    print("Current URL:", driver.current_url)
    print("Page HTML snippet:\n", driver.page_source[:500]) 
    box = driver.find_element(By.ID, "password-textbox")  # assumes input has id="password"
    box.send_keys(password)
    go_button = driver.find_element(By.ID, "submit-button")  # assumes button has id="go"
    go_button.click()
    time.sleep(2)
    view_button = driver.find_element(By.ID, "location-button")  # assumes id="view"
    view_button.click()
    time.sleep(2)
    img_element = driver.find_element(By.ID, "image")
    img_url = img_element.get_attribute("src")
    img_data = requests.get(img_url).content
    with open("Current_Location.jpg", "wb") as f:
        f.write(img_data)
    location_text = driver.find_element(By.ID, "location").text
    return location_text