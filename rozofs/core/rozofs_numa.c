/*
  Copyright (c) 2010 Fizians SAS. <http://www.fizians.com>
  This file is part of Rozofs.

  Rozofs is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published
  by the Free Software Foundation, version 2.

  Rozofs is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see
  <http://www.gnu.org/licenses/>.
 */
#include <numa.h>
#include "rozofs_numa.h"
#include <rozofs/common/common_config.h>

/**
*  case of NUMA: allocate the running node according to the
*  instance

   @param instance: instance number of the process
*/
void rozofs_numa_allocate_node(int instance)
{
   int configured_nodes;
   int available;
   int bit;
   
   if (!common_config.numa_aware) {
     return;
   }  
   
   available = numa_available();
   if (available < 0)
   {
     /*
     ** numa not available
     */
     return;
   }
     
   configured_nodes = numa_num_configured_nodes();   
   bit = instance%configured_nodes;
   numa_run_on_node(bit); 
   /*
   ** set the preferred memory
   */
   numa_set_preferred(bit);

}
