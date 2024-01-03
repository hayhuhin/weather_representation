import plotly.express as px
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go




class GraphRepresantation(object):
    """
    this class is a wrapper for the plotly library.
    class is used for returning plotly graphs in much easier and cleaner way
    each method is returning graph as image or html

    Attributes:
      presentation(str) : default value is "card"(not used for now)

    Methods:
      graph_option(graph_type:str,dict_values:dict,path=None,to_html=True)
        controller method that calling other methods by the given graph_type
        example:if the given graph type is "bar_graph" then it will call the bar_graph fill the args and return the result
      bar_graph(dict_values:dict,path=None,to_html=True,compare=False)
        unpacking the dict values and pushing it to the plotly library functions
        that creates the graph representation(can return image or html)
      pie_graph(values:list,names:list,path=None,to_html=True)
        passing the values and names into the plotly class to create
        pie graph and represent it as image or html
      line_graph(dict_values:dict,path=None,to_html=True,compare=False)
        unpacking the dict values and pushing it to the plotly library functions
        that creates the graph representation(can return image or html)
      donut_graph(values:list,names:list,path=None,to_html=True)
        passing the values and names into the plotly class to create
        donut graph and represent it as image or html
      user_card(user_data:dict)
        cretes html simple block representation with user data
      graph_card(user_data:dict,user_calc)
        cretes html simple block representation with user data
    """

    def __init__(self,presentation:str='card'):
        """
        Constructor method for GraphRepresantation.

        Args:
          self.presentation(str):default value is 'card'
          self.template (str) : changing the plotly graph background
          self.current_path(object) : this path is the path where to store the graphs if displayed as picture
        """
        self.presentation = presentation
        self.template = 'plotly_dark'
        self.currant_path = Path.cwd()
        self.graph_repr_sizes = {"1_row":{"x":900,"y":500},"2_row":{"x":480,"y":300}}

        self.visuals_data = {"paper_bgcolor":"rgba(0,0,0,0)",
                              "plot_bgcolor": "rgba(0, 0, 0, 0)",
                              "modebar":{'bgcolor':'rgba(0, 0, 0, 0)'}
        }


    def graph_options(self,graph_type:str,dict_values:dict,graph_repr:str,path=None,to_html=True):
        """
        method that gives you the option to choose which graph to represent by the graph_type
        arg that must be the same as the name of the func (example:"graph_type")
        this method calling other methods by the graph type arg and returns the method result

        Args:
          graph_type(str):accepts on of graph represantations the user chooses "bar_graph","line_grap"
          dict_values(dict):accepts dict that contains the keys:x(str/int),y(int),y_2(int)
          path=None : the path to save the image of the graph if to_html=False
          to_html=True: if True returns all graphs figures as html/if false returns figures as image

        Returns:
          HTML string represantation 
        """

        #this method validating the inputs of the user(its called each time the graph_option called) returns True if validated
        validated = self.validate_inputs(dict_values=dict_values,graph_repr=graph_repr,path=path)

        if validated:      
          if graph_type == self.bar_graph.__name__:
              return self.bar_graph(dict_values=dict_values,path=path,to_html=to_html,graph_repr=graph_repr)
          if graph_type == self.pie_graph.__name__:
              return self.pie_graph(dict_values=dict_values,path=path,to_html=to_html)
          if graph_type == self.donut_graph.__name__:
              return self.donut_graph(dict_values=dict_values,path=path,to_html=to_html)
          if graph_type == self.line_graph.__name__:
              return self.line_graph(dict_values=dict_values,path=path,to_html=to_html,graph_repr=graph_repr)
          if graph_type == "bar_graph_compared":
              return self.bar_graph(dict_values=dict_values,path=path,to_html=to_html,compare=True,graph_repr=graph_repr)
          if graph_type == "line_graph_compared":
              return self.line_graph(dict_values=dict_values,path=path,to_html=to_html,compare=True,graph_repr=graph_repr)
          else:
              raise ValueError("the correct value must be existing graph type")


    def bar_graph(self,dict_values:dict,graph_repr:str,path:str=None,to_html=True,compare=False):
        """
        extracting dict values and passing them into plotly bar figure.
        can return image or html string represantation

        args:
          dict_values(dict):
            contains x(str/int) : most of the time its the x line on the graphs.
            contains y(int) : its the y line on the graphs.
            if compare=True it can contain y_2 as a compare y value.
          path: only used to_html=False and saving the pic in specified path
          to_html : default is true and returns the graph as html repr so it can be loaded in the html template
        
        
        Returns:
          HTML string representation
        """

        #checking the required bar sizes 
        if graph_repr in self.graph_repr_sizes:
            x_size = self.graph_repr_sizes[graph_repr]["x"]
            y_size = self.graph_repr_sizes[graph_repr]["y"]


            #creating dataframe for the graph figure
            data_frame = pd.DataFrame(dict(group=dict_values["x"],value=dict_values["y"]))
            #creating the right graph figure(bar graph)and passing the data frame created
            graph_fig = px.bar(data_frame,x='group',y='value',template=self.template)
            #updating some visuals for the graph and the size
            graph_fig.update_layout(paper_bgcolor=self.visuals_data["paper_bgcolor"],
                                    plot_bgcolor= self.visuals_data["plot_bgcolor"],
                                    modebar=self.visuals_data["modebar"],
                                    # width=x_size,
                                    height=y_size,
    )        #updating the textfont size
            graph_fig.update_traces(textfont_size=12)
            #adding angle for the months keys
            graph_fig.update_xaxes(
              tickangle=-45,#the angle of the presentation
              dtick="M1", # sets minimal interval to month
              tickformat="%d.%m.%Y", # the date format you want 
    )
            #here its checking if the data have to be compared
            if compare:

              #creating the right graph figure(bar graph)and passing the data frame created
              graph_fig = px.bar(
                  x=dict_values["x"],
                  y=[dict_values["y"], dict_values["y_2"]],
                  labels={'value': 'Income', 'x':'Date','variable': 'amount'},
                  title=f"blue is {dict_values['DB_1']} orange is {dict_values['DB_2']}",
                  color_discrete_sequence=['blue', 'orange'],  # Set custom colors
                  template=self.template,
              )

              graph_fig.update_layout(barmode='group',
                                      paper_bgcolor=self.visuals_data["paper_bgcolor"],
                                      plot_bgcolor= self.visuals_data["plot_bgcolor"],
                                      modebar=self.visuals_data["modebar"],
                                      # width=x_size,
                                      height=y_size,
                                      bargap=0.2,
                                      bargroupgap=0.2,
              )

              graph_fig.update_traces(textfont_size=12)

              graph_fig.update_xaxes(
                tickangle=-45,#the angle of the presentation
                dtick="M1", # sets minimal interval to month
                tickformat="%d.%m.%Y",) # the date format you want 
              
              graph = graph_fig.to_html(config={'displayModeBar': True})
              return graph
            
            if to_html:
                graph = graph_fig.to_html(config={'displayModeBar': True})
            else:
                graph = graph_fig.write_image(path)
            return graph
        

    def line_graph(self,dict_values:dict,graph_repr:str,path:str=None,to_html=True,compare=False):
        """
        extracting dict values and passing them into plotly line figure.
        can return image or html string represantation

        args:
          dict_values(dict):
            contains x(str/int) : most of the time its the x line on the graphs.
            contains y(int) : its the y line on the graphs.
            if compare=True it can contain y_2 as a compare y value.
          path: only used to_html=False and saving the pic in specified path
          to_html : default is true and returns the graph as html repr so it can be loaded in the html template
        
        Returns:
          HTML string representation
        """

        #first checking if the graph_repr in the graph repr sizes

        if graph_repr in self.graph_repr_sizes:
          x_size = self.graph_repr_sizes[graph_repr]["x"]
          y_size = self.graph_repr_sizes[graph_repr]["y"]



          group = dict_values["x"]
          value = dict_values["y"]

          path = str(self.currant_path) +"/employer_profile/static/employer/images/pie.png"
          line_fig = px.line(y=value,x=group,template=self.template)
          line_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor = "rgba(0,0,0,0)",
                                modebar={'bgcolor':'rgba(0, 0, 0, 0)'},
                                # width=x_size,
                                # height=y_size
                                )
          line_fig.update_traces(textfont_size=12,text='percent+label')
          line_fig.update_xaxes(tickangle=-45)

          if compare:
              
            dict_values
            values_1 = dict_values["y"]
            values_2 = dict_values["y_2"]
            group = dict_values["x"]

            line_fig = px.line(
                x=group,
                y=[values_1, values_2],
                labels={'value': 'Income', 'x':'Date',},
                  title=f"blue is {dict_values['DB_1']} orange is {dict_values['DB_2']}",
                color_discrete_sequence=['blue', 'orange'],  # Set custom colors
                template=self.template,
            )

            # fig.update_layout(barmode='group')
            # graph_fig = px.bar(data_frame,x='group',y='value',template=self.template)
            line_fig.update_layout(barmode='group',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                    modebar={'bgcolor':'rgba(0, 0, 0, 0)'},
                                    bargap=0.2,
                                    bargroupgap=0.2,
                                    width=x_size,
                                    height=y_size
                                    )


            line_fig.update_traces(textfont_size=12)

            line_fig.update_xaxes(
              tickangle=-45,#the angle of the presentation
              dtick="M1", # sets minimal interval to month
              tickformat="%d.%m.%Y",) # the date format you want 
            
            graph = line_fig.to_html(config={'displayModeBar': True})
            return graph



          if to_html:
              graph = line_fig.to_html(config={'displayModeBar': True})
          else:
              graph = line_fig.write_image(path)
          return graph


    def validate_inputs(self,dict_values:dict,graph_repr:str,path:str=None,):
        """
        method that called once in the graph_option method to check if the input is the right type
        this method validated and tested in the test.py file

        Args:
          dict_values(dict):accepts dict that contains the keys:x(str/int),y(int),y_2(int).
          graph_repr(str) : accepts only str.
          path(str) or None:accepts None or str path.

        Returns:
          validates the fields and raises Value error with message if not validate
          if the values are valid it will return True
        """

        #first we are validating the dict_values(they must in the list)
        proper_values = ["graph_title","graph_description","graph_type","created_at","x","y","y_2","start_date","end_date","position","DB_1","DB_2","sql_database_compared","sql_database"]

        for key in dict_values:
            if key in proper_values:
                continue
            else:
                raise ValueError("the key name is invalid")
        #creating for loop with o(n) time complexity

        #iterating over the len of dict x (it will always be the same length as y or y_2)
        for index in range(len(dict_values["x"])):
            #check the x type
            if not isinstance(dict_values["x"][index],(str,float)):
              raise ValueError("x/y/y_2 value types are invalid")

            #check the y type
            if not isinstance(dict_values["y"][index],int):
                raise ValueError("x/y/y_2 value types are invalid")
            
            #check if the y_2 compare is existing
            # if "y_2" in dict_values:
            #     if not isinstance(dict_values["y_2"][index],int):
            #       raise ValueError("x/y/y_2 value types are invalid")
                
        # #check if the y_2 exists
        # if "y_2" in dict_values:
        #     #if y_2 exists and if the len is the same
        #     if len(dict_values["y_2"]) != len(dict_values["x"]):
        #         raise ValueError("len x is not the same as y")
        #check if the len(x) same as len(y)
        if len(dict_values["x"]) != len(dict_values["y"]):
            raise ValueError("len x is not the same as y")

        #check path type 
        if path:
          if not isinstance(path,(str)):
              raise ValueError("not str type")

        #check if graph_repr is not str
        if not isinstance(graph_repr,(str)):
            raise ValueError("not str type")


        #if it passed all the validations it will return True
        return True
 

    def pie_graph(self,values:list,names:list,path:str=None,to_html=True):
        """
        extracting values and passing them into plotly pie figure.
        can return image or html string represantation

        args:
          names(list) :contains x(str/int) : most of the time its the x line on the graphs.
          value(list) :scontains y(int) : its the y line on the graphs.
            if compare=True it can contain y_2 as a compare y value.
          path: only used to_html=False and saving the pic in specified path
          to_html : default is true and returns the graph as html repr so it can be loaded in the html template

        Returns:
          HTML string representation
        """

        path = str(self.currant_path) +"/employer_profile/static/employer/images/pie.png"

        pie_fig = px.pie(values=values,names=names,template=self.template)
        pie_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        pie_fig.update_traces(textfont_size=12,textinfo='percent+label')


        if to_html:
            graph = pie_fig.to_html(config={'displayModeBar': True})
        else:
            graph = pie_fig.write_image(path)
        return graph


    def donut_graph(self,values:list,names:list,path:str=None,to_html=True):
        """this method return the donut graph 
            Args:
              group: most of the time its the x line on the graphs
              value: its the y line on the graphs
              path: only used to_html=False and saving the pic in specified path
              to_html : default is true and returns the graph as html repr so it can be loaded in the html template
 
            Returns:
              HTML string representation
        """
        path = str(self.currant_path) +"/employer_profile/static/employer/images/donut.png"

        donut_fig = px.pie(values = values,template=self.template,
                names = names,
                # color = ['G1', 'G2', 'G3', 'G4'],
                hole = 0.5,
                width=400,
                )
        #the bg color of the pie
        donut_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=0,r=20,t=20,b=20))
        #text position and the font size udjustments
        donut_fig.update_traces(textfont_size=12,textinfo='percent+label')#textposition="outside",
        if to_html:
            graph = donut_fig.to_html(config={'displayModeBar': True})
        
        else:
            graph = donut_fig.write_image(path)
        return graph
    

    def user_card(self,user_data:dict):
        """
        returns html card with the user data that recieved from the user_data
        the user data must contain 'username','user_position','picture' as a 
        dict

        Args:
          user_data(dict):must contain 'username','user_position'and 'picture' keys with values

        Returns:
          HTML string representation
        """

        username = user_data['username']
        user_position = user_data['job_position']
        profile_pic = user_data['profile_pic']
        card_html = """<div class="">
        <div class="">

          <img

            src={}
            class="rounded-5 mb-3"
            style="height:225px"
            alt="employer picture"
          />

          <h3 class="text-capitalize mb-2">{}</h3>
        <div class="text-capitalize">
          <a class="nav-link dropdown-toggle mb-5" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            edit details
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">contact details</a></li>
            <li><a class="dropdown-item" href="#">department details</a></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>


          <h5 class="mt-5 mb-3">contact details</h5>
           
          <p class="card-text">phone number: +973 552251273 </p>
          <p class="card-text">position: {} department</p>
          <p class="card-text">department contact number: +1 47577226</p>
          <p class="card-text">department address: vaizman 24 tel-aviv </p>

          <h5 class="mt-5 mb-3">personal details</h5>
          <p class="card-text">age: 33</p>
          <p class="card-text">address: anilevich 28 holon </p>
          <p class="card-text">workers: 0</p>
          <p class="card-text">manager: valeri levinson</p>
          <p class="card-text">department manager: arg argus</p>
          <p class="card-text">description: none</p>

        </div>

      </div>

        <div class="card-footer text-body-secondary">
          <div class="container">
            <div class="row">
              <div class="col-sm-auto" style="margin-top: 15px">
                <a href="#" class="btn btn-success">EDIT</a>
              </div>
            </div>
            </div>
            </div>
          
          
        </div>""".format(profile_pic,username,user_position)
        
        return card_html
  

    def graph_card(self,user_data:dict,user_calc:str):
        """
        returns html card with the user data that recieved from the user_data and user_calc
        the user data must contain 'username','user_position','picture' as a 
        dict

        Args:
          user_data(dict):must contain 'username','user_position'and 'picture' keys with values

        Returns:
          HTML string representation
        """
        card_html = """<div class="col"style='width:350px;height:450px'>
                          <div class="ms-3"> 
                          <p class="text-secondary fs-5">- {}</p>
                          <div name="plotly_element">{}</div>
                        </div>
                            </div>""".format(user_data,user_calc)
        
        return card_html
    

    